from abc import ABC, abstractmethod
from typing import Any

class ISimilarity(ABC):
    @abstractmethod
    async def process_document(self, document_data: bytes) -> Any:

        pass

    @abstractmethod
    async def process_text(self, text: str) -> Any:

        pass