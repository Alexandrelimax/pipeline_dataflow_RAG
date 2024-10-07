from abc import ABC, abstractmethod

class ChunkExtractorStrategy(ABC):
    
    @abstractmethod
    def extract_chunks_from_document(self, file_path, start_chunk=4, end_chunk=10):
        raise NotImplementedError("This method should be overridden by subclasses")