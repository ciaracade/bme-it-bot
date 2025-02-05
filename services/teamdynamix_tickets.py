from config.teamdynamix import get_config
import requests
from datetime import datetime
from services.openai_service import OpenAIService
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from services.database_service import DatabaseService

class TeamDynamixTickets:
    def __init__(self):
        self.config = get_config()
        self.base_url = self.config['base_url']
        self.endpoints = self.config['endpoints']
        self.auth = TeamDynamixAuth(self.config)
        self.session = None
        self.ai_service = OpenAIService()
        self.openai_service = OpenAIService()
        self.db_service = DatabaseService()

    async def _ensure_authenticated(self):
        """Ensure we have an authenticated session"""
        if not self.session:
            auth_success = await self.auth.authenticate()
            if auth_success:
                self.session = self.auth.session
            else:
                raise Exception("Failed to authenticate with TeamDynamix")
        return self.session

    def _extract_first_name(self, email_address):
        """Extract first name from email address or full name"""
        # Handle format: "First Last <email@umich.edu>"
        if '<' in email_address:
            full_name = email_address.split('<')[0].strip()
            first_name = full_name.split()[0]  # Get first word of full name
            return first_name
        # Handle format: email@umich.edu
        return email_address.split('@')[0]

    def _format_ticket_title(self, first_name, description):
        """Format ticket title according to BME IT standards"""
        return f"{first_name} / {description}"

    async def create_ticket(self, email_address, description, priority=None, is_emergency=False):
        """Create a new ticket with AI assistance"""
        first_name = self._extract_first_name(email_address)
        
        # Get AI solution
        solution, solution_id = await self.openai_service.get_completion(
            description,
            ticket_id=None
        )
        
        # Create ticket with solution
        title = self._format_ticket_title(first_name, description)
        ticket_data = {
            "Title": title,
            "Description": f"{description}\n\nAI Solution:\n{solution}",
            "RequestorEmail": email_address.split('<')[-1].strip('>') if '<' in email_address else email_address,
            "StatusID": self._get_default_status_id(),
            "PriorityID": priority or self._get_default_priority_id(),
            "CreatedDate": datetime.utcnow().isoformat(),
            "Source": "Slack Bot - AI Assisted",
            "Attributes": {
                "RequesterName": first_name,
                "SolutionID": solution_id  # Store solution ID in ticket attributes
            }
        }

        response = await self._ensure_authenticated()
        response = response.post(f"{self.base_url}{self.endpoints['tickets']}", json=ticket_data)
        response.raise_for_status()
        return response.json()

    async def get_ticket(self, ticket_id):
        """Retrieve ticket details"""
        endpoint = f"{self.base_url}{self.endpoints['tickets']}/{ticket_id}"
        response = await self._ensure_authenticated()
        response = response.get(endpoint)
        response.raise_for_status()
        return response.json()

    async def update_ticket(self, ticket_id, updates):
        """Update an existing ticket"""
        endpoint = f"{self.base_url}{self.endpoints['tickets']}/{ticket_id}"
        response = await self._ensure_authenticated()
        response = response.patch(endpoint, json=updates)
        response.raise_for_status()
        return response.json()

    async def add_comment(self, ticket_id, comment, is_private=False):
        """Add a comment to a ticket"""
        endpoint = f"{self.base_url}{self.endpoints['tickets']}/{ticket_id}/comments"
        
        comment_data = {
            "Comment": comment,
            "IsPrivate": is_private,
            "CreatedDate": datetime.utcnow().isoformat()
        }

        response = await self._ensure_authenticated()
        response = response.post(endpoint, json=comment_data)
        response.raise_for_status()
        return response.json()

    async def search_tickets(self, query):
        """Search for tickets based on criteria"""
        endpoint = f"{self.base_url}{self.endpoints['tickets']}/search"
        response = await self._ensure_authenticated()
        response = response.post(endpoint, json=query)
        response.raise_for_status()
        return response.json()

    def _get_default_status_id(self):
        # Configure this based on your TeamDynamix setup
        return self.config.get('default_status_id', 1)  # Example default

    def _get_default_priority_id(self):
        # Configure this based on your TeamDynamix setup
        return self.config.get('default_priority_id', 1)  # Example default

    async def get_my_tickets(self, email):
        """Get all tickets created by or assigned to a user"""
        query = {
            "SearchText": "",
            "RequestorEmail": email,
            "IsActive": True,
            "MaxResults": 10
        }
        return await self.search_tickets(query)

    async def get_recent_updates(self, ticket_id, limit=5):
        """Get recent updates/comments for a ticket"""
        endpoint = f"{self.base_url}{self.endpoints['tickets']}/{ticket_id}/feed"
        response = await self._ensure_authenticated()
        response = response.get(endpoint)
        response.raise_for_status()
        return response.json()[:limit]

    async def assign_ticket(self, ticket_id, assignee_email):
        """Assign a ticket to a specific user"""
        updates = {
            "ResponsibleEmail": assignee_email,
            "StatusID": self.config['status_ids'].get('assigned', self._get_default_status_id())
        }
        return await self.update_ticket(ticket_id, updates)

    async def close_ticket(self, ticket_id, resolution):
        """Close a ticket with a resolution"""
        updates = {
            "StatusID": self.config['status_ids'].get('closed'),
            "Resolution": resolution,
            "ResolutionDate": datetime.utcnow().isoformat()
        }
        return await self.update_ticket(ticket_id, updates)

    async def categorize_ticket(self, title, description):
        """Use AI to categorize the ticket and suggest priority"""
        prompt = f"""
        Based on this IT support ticket:
        Title: {title}
        Description: {description}
        
        Categorize this ticket and suggest a priority level with emergency status.
        
        Categories: Hardware, Software, Network, Access/Permissions, Other
        Priority Levels: Low, Medium, High
        Emergency Status: Add SOS if this involves:
        - Server downtime
        - Network security threats
        - Malicious activity
        - Critical system failures
        
        Format response as:
        Category: [category]
        Priority: [priority]
        Emergency: [Yes/No]
        Reasoning: [explanation]
        """
        
        suggestion = await self.ai_service.get_completion(prompt)
        return suggestion

    async def get_tickets_by_assignee(self, assignee_email):
        """Get all tickets assigned to a specific worker"""
        query = {
            "ResponsibleEmail": assignee_email,
            "IsActive": True,
            "MaxResults": 50  # Adjust as needed
        }
        return await self.search_tickets(query)

    def _get_priority_indicator(self, priority, is_emergency=False):
        """Get emoji indicator based on priority and emergency status"""
        base_indicators = {
            'High': '🔴',
            'Medium': '🟠',
            'Low': '🟢'
        }
        # Add SOS indicator for emergency tickets
        if is_emergency:
            return f"🆘 {base_indicators.get(priority, '⚪')}"
        return base_indicators.get(priority, '⚪')

class TeamDynamixAuth:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BME-IT-SlackBot/1.0',
        })

    async def authenticate(self):
        """Authenticate through U-M's SSO to TeamDynamix"""
        try:
            # 1. Initial request to TeamDynamix to get redirected to U-M Login
            response = self.session.get(f"{self.config['base_url']}/TDWebApi/")
            
            # 2. Follow redirect to U-M WebLogin
            login_url = response.url  # Should be weblogin.umich.edu
            
            # 3. Submit credentials to U-M WebLogin
            login_data = {
                'login': self.config['username'],
                'password': self.config['password'],
                'AuthMethod': 'FormsAuthentication'
            }
            
            # Get any hidden form fields needed for authentication
            soup = BeautifulSoup(response.text, 'html.parser')
            for input_tag in soup.find_all('input', type='hidden'):
                login_data[input_tag['name']] = input_tag['value']
            
            # Submit login form
            auth_response = self.session.post(login_url, data=login_data)
            
            # 4. Handle Duo 2FA if required
            if 'duo' in auth_response.url.lower():
                raise NotImplementedError("Duo 2FA handling needs to be implemented")
            
            # 5. Follow redirects back to TeamDynamix
            if auth_response.ok:
                # Get API token or session cookie
                api_token = self._extract_api_token(auth_response)
                self.session.headers.update({
                    'Authorization': f'Bearer {api_token}',
                    'Content-Type': 'application/json'
                })
                return True
            
            return False

        except Exception as e:
            print(f"Authentication failed: {e}")
            return False

    def _extract_api_token(self, response):
        """Extract API token from authenticated response"""
        # This will depend on how TeamDynamix provides the token
        # You might need to make an additional API call or parse it from headers/cookies
        try:
            # Example - adjust based on actual TeamDynamix response
            token_match = re.search(r'ApiToken["\']:\s*["\']([^"\']+)', response.text)
            if token_match:
                return token_match.group(1)
            
            # Alternative: might be in a cookie or header
            return self.session.cookies.get('TDWebApi_Auth')
        except Exception:
            return None 