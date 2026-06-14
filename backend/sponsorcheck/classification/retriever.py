from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
from sponsorcheck.data.soc_store import get_soc_store
from sponsorcheck.domain.models import SocCandidate

class SocRetriever:
    _instance = None

    def __init__(self):
        self.store = get_soc_store()
        self.records = self.store.get_all()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self._build_index()

    def _build_index(self):
        # Use the search_text field for TF-IDF if it exists, otherwise job_type and related_job_titles
        corpus = []
        for r in self.records:
            if r.search_text:
                corpus.append(r.search_text)
            else:
                text = f"{r.occupation_code} {r.job_type} {' '.join(r.related_job_titles)}"
                corpus.append(text)
        
        if corpus:
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    @classmethod
    def get_instance(cls) -> "SocRetriever":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def retrieve(self, query: str, top_k: int = 15) -> List[SocCandidate]:
        if not query.strip() or not self.records:
            return []
            
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        candidates = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score > 0.0:
                record = self.records[idx]
                
                # safely extract eligibility
                eligibility_val = None
                if isinstance(record.eligibility, dict):
                    eligibility_val = record.eligibility.get("raw")
                elif isinstance(record.eligibility, str):
                    eligibility_val = record.eligibility
                    
                candidate = SocCandidate(
                    occupation_code=record.occupation_code,
                    job_type=record.job_type,
                    score=score,
                    eligibility=eligibility_val,
                    rates=record.rates,
                    special_salary_routes=record.special_salary_routes
                )
                candidates.append(candidate)
                
        return candidates

def get_retriever() -> SocRetriever:
    return SocRetriever.get_instance()
