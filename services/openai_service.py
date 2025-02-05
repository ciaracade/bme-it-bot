from openai import AsyncOpenAI
from config.settings import get_settings
from services.google_drive_service import GoogleDriveService
from services.database_service import DatabaseService
from typing import List, Dict, Optional
from models.solution import Solution

class OpenAIService:
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.drive_service = GoogleDriveService()
        self.db_service = DatabaseService()
        
    async def get_completion(self, prompt: str, ticket_id: str = None) -> tuple[str, Optional[int]]:
        """Get AI completion with documentation and solution database support"""
        try:
            # Search documentation
            docs = await self.drive_service.search_documentation(prompt)
            
            # Search solution database
            solutions = await self.db_service.search_solutions(prompt)
            
            # Create enhanced prompt
            enhanced_prompt = self._create_enhanced_prompt(prompt, docs, solutions)
            
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a helpful IT support assistant for the University of Michigan Biomedical Engineering department.
                        Use the provided documentation and past solutions to inform your responses."""
                    },
                    {
                        "role": "user",
                        "content": enhanced_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            solution = response.choices[0].message.content
            solution_id = None
            
            # Store the new solution if ticket_id is provided
            if ticket_id:
                new_solution = await self.db_service.add_solution(
                    ticket_id=ticket_id,
                    problem=prompt,
                    solution=solution,
                    category=self._determine_category(prompt),
                    keywords=self._extract_keywords(prompt)
                )
                solution_id = new_solution.id
            
            return solution, solution_id
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}", None

    def _create_enhanced_prompt(self, original_prompt: str, docs: List[Dict], solutions: List[Solution]) -> str:
        """Create prompt enhanced with documentation and past solutions"""
        enhanced_prompt = f"""Based on the following information, please help with this issue:

Question: {original_prompt}

"""
        if docs:
            enhanced_prompt += "\nRelevant Documentation:\n"
            for doc in docs:
                enhanced_prompt += f"\nFrom '{doc['title']}':\n{doc['content'][:500]}...\n"

        if solutions:
            enhanced_prompt += "\nRelevant Past Solutions:\n"
            for solution in solutions:
                enhanced_prompt += f"\nSimilar Problem: {solution.problem_description}\nSolution: {solution.solution_description}\n"

        enhanced_prompt += "\nPlease provide a solution based on this information and best practices."
        return enhanced_prompt

    def _determine_category(self, prompt: str) -> str:
        # Implementation of _determine_category method
        pass

    def _extract_keywords(self, prompt: str) -> List[str]:
        # Implementation of _extract_keywords method
        pass 