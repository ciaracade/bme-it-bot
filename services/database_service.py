from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.solution import Base, Solution
from typing import List, Optional
import logging
from datetime import datetime
from models.feedback import SolutionFeedback

class DatabaseService:
    def __init__(self, database_url: str = "sqlite:///solutions.db"):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    async def add_solution(self, 
                         ticket_id: str,
                         problem: str,
                         solution: str,
                         category: str,
                         source: str = 'ai_generated',
                         keywords: List[str] = None):
        """Add a new solution to the database"""
        try:
            session = self.Session()
            new_solution = Solution(
                ticket_id=ticket_id,
                problem_description=problem,
                solution_description=solution,
                category=category,
                keywords=','.join(keywords) if keywords else '',
                source=source
            )
            session.add(new_solution)
            session.commit()
            return new_solution
        except Exception as e:
            logging.error(f"Error adding solution: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    async def search_solutions(self, query: str, limit: int = 5) -> List[Solution]:
        """Search for solutions based on problem description or keywords"""
        try:
            session = self.Session()
            solutions = session.query(Solution).filter(
                (Solution.problem_description.ilike(f"%{query}%")) |
                (Solution.keywords.ilike(f"%{query}%"))
            ).order_by(Solution.success_rate.desc()).limit(limit).all()
            return solutions
        finally:
            session.close()

    async def update_solution_success(self, solution_id: int, was_successful: bool):
        """Update solution success rate"""
        try:
            session = self.Session()
            solution = session.query(Solution).get(solution_id)
            if solution:
                solution.usage_count += 1
                # Update success rate using weighted average
                solution.success_rate = (
                    (solution.success_rate * (solution.usage_count - 1) + 
                     (1.0 if was_successful else 0.0)) / solution.usage_count
                )
                solution.updated_at = datetime.utcnow()
                session.commit()
        finally:
            session.close()

    async def get_similar_solutions(self, problem: str, threshold: float = 0.5) -> List[Solution]:
        """Get similar solutions using text similarity"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        try:
            session = self.Session()
            all_solutions = session.query(Solution).all()
            
            if not all_solutions:
                return []

            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer()
            all_problems = [s.problem_description for s in all_solutions]
            all_problems.append(problem)
            tfidf_matrix = vectorizer.fit_transform(all_problems)
            
            # Calculate similarity
            similarities = cosine_similarity(
                tfidf_matrix[-1:], tfidf_matrix[:-1]
            )[0]
            
            # Get solutions above threshold
            similar_solutions = [
                solution for solution, similarity in zip(all_solutions, similarities)
                if similarity >= threshold
            ]
            
            return sorted(similar_solutions, 
                        key=lambda x: x.success_rate * similarities[all_solutions.index(x)],
                        reverse=True)
        finally:
            session.close() 

    async def add_feedback(self, 
                          solution_id: int, 
                          ticket_id: str, 
                          was_helpful: bool, 
                          feedback_text: str = None,
                          user_email: str = None):
        """Add feedback for a solution"""
        try:
            session = self.Session()
            feedback = SolutionFeedback(
                solution_id=solution_id,
                ticket_id=ticket_id,
                was_helpful=was_helpful,
                feedback_text=feedback_text,
                user_email=user_email
            )
            session.add(feedback)
            
            # Update solution success rate
            solution = session.query(Solution).get(solution_id)
            if solution:
                await self.update_solution_success(solution_id, was_helpful)
            
            session.commit()
            return feedback
        except Exception as e:
            logging.error(f"Error adding feedback: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    async def get_solution_stats(self, solution_id: int):
        """Get statistics for a solution"""
        try:
            session = self.Session()
            solution = session.query(Solution).get(solution_id)
            if not solution:
                return None

            feedback = session.query(SolutionFeedback).filter_by(solution_id=solution_id).all()
            
            return {
                'total_uses': len(feedback),
                'helpful_count': sum(1 for f in feedback if f.was_helpful),
                'success_rate': solution.success_rate,
                'recent_feedback': [f.feedback_text for f in feedback[-5:] if f.feedback_text]
            }
        finally:
            session.close() 