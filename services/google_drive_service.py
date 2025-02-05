from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import PyPDF2
from google.oauth2 import service_account
import os
from typing import List, Dict
import logging
from services.cache_service import CacheService

class GoogleDriveService:
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_file(
            'config/google_credentials.json',
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        self.service = build('drive', 'v3', credentials=self.credentials)
        self.documentation_folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        self.cache = CacheService(cache_dir="cache/drive_docs", ttl_hours=24)

    async def search_documentation(self, query: str) -> List[Dict]:
        """Search documentation for relevant content"""
        try:
            # Search in Drive folder
            results = []
            page_token = None
            while True:
                response = self.service.files().list(
                    q=f"'{self.documentation_folder_id}' in parents and trashed=false",
                    spaces='drive',
                    fields='nextPageToken, files(id, name, mimeType)',
                    pageToken=page_token
                ).execute()

                for file in response.get('files', []):
                    content = await self._get_file_content(file)
                    if self._content_matches_query(content, query):
                        results.append({
                            'title': file['name'],
                            'content': content,
                            'relevance': self._calculate_relevance(content, query)
                        })

                page_token = response.get('nextPageToken')
                if not page_token:
                    break

            # Sort by relevance
            results.sort(key=lambda x: x['relevance'], reverse=True)
            return results[:3]  # Return top 3 most relevant results

        except Exception as e:
            logging.error(f"Error searching documentation: {e}")
            return []

    async def _get_file_content(self, file: Dict) -> str:
        """Extract content from a file, with caching"""
        # Try to get from cache first
        cached_content = self.cache.get(file['id'])
        if cached_content:
            return cached_content

        try:
            if file['mimeType'] == 'application/pdf':
                content = await self._extract_pdf_content(file['id'])
            else:  # Google Doc
                content = await self._extract_doc_content(file['id'])

            # Cache the content
            self.cache.set(file['id'], content)
            return content

        except Exception as e:
            logging.error(f"Error extracting content from {file['name']}: {e}")
            return ""

    async def _extract_pdf_content(self, file_id: str) -> str:
        """Extract text from PDF file"""
        request = self.service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            _, done = downloader.next_chunk()

        file.seek(0)
        pdf_reader = PyPDF2.PdfReader(file)
        return " ".join(page.extract_text() for page in pdf_reader.pages)

    async def _extract_doc_content(self, file_id: str) -> str:
        """Extract text from Google Doc"""
        doc = self.service.files().export(
            fileId=file_id,
            mimeType='text/plain'
        ).execute()
        return doc.decode('utf-8')

    def _content_matches_query(self, content: str, query: str) -> bool:
        """Check if content is relevant to query"""
        query_terms = query.lower().split()
        content_lower = content.lower()
        return all(term in content_lower for term in query_terms)

    def _calculate_relevance(self, content: str, query: str) -> float:
        """Calculate relevance score of content to query"""
        query_terms = query.lower().split()
        content_lower = content.lower()
        
        # Simple scoring based on term frequency
        score = sum(content_lower.count(term) for term in query_terms)
        
        # Boost score if terms appear close together
        if all(term in content_lower for term in query_terms):
            score *= 1.5
            
        return score 

    # Add method to refresh cache for specific files
    async def refresh_cache(self, file_ids: List[str] = None):
        """Refresh cache for specified files or all files in documentation folder"""
        try:
            if not file_ids:
                # Get all files in documentation folder
                response = self.service.files().list(
                    q=f"'{self.documentation_folder_id}' in parents and trashed=false",
                    fields='files(id, name, mimeType)'
                ).execute()
                file_ids = [file['id'] for file in response.get('files', [])]

            for file_id in file_ids:
                self.cache.clear(file_id)
                file = self.service.files().get(fileId=file_id).execute()
                await self._get_file_content(file)

        except Exception as e:
            logging.error(f"Cache refresh error: {e}") 