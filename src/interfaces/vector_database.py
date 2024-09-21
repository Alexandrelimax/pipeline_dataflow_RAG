from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorDatabase(ABC):
    
    @abstractmethod
    def create_table(self) -> None:
        pass

    @abstractmethod
    def save_embeddings(self, embeddings: List[Dict[str, Any]]) -> None:
        pass

    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
        pass

