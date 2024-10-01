from abc import ABC, abstractmethod

class DocumentLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> str:
        pass