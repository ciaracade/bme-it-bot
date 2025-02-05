from datetime import datetime, timedelta
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SolutionAnalysisService:
    def __init__(self, db_service):
        self.db_service = db_service

    async def analyze_solutions(self):
        """Analyze solution effectiveness and patterns"""
        session = self.db_service.Session()
        try:
            # Get all solutions with feedback
            solutions = session.query(Solution).all()
            
            # Convert to pandas for analysis
            df = pd.DataFrame([{
                'id': s.id,
                'problem': s.problem_description,
                'solution': s.solution_description,
                'success_rate': s.success_rate,
                'usage_count': s.usage_count,
                'category': s.category
            } for s in solutions])
            
            # Analyze patterns in successful solutions
            successful = df[df['success_rate'] > 0.8]
            
            # Find common patterns
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(successful['solution'])
            
            return {
                'total_solutions': len(solutions),
                'successful_solutions': len(successful),
                'avg_success_rate': df['success_rate'].mean(),
                'top_categories': df.groupby('category')['success_rate'].mean().sort_values(ascending=False),
                'common_terms': dict(zip(
                    vectorizer.get_feature_names_out(),
                    tfidf_matrix.sum(axis=0).A1
                ))
            }
            
        finally:
            session.close() 