from src.interfaces.document_loader import DocumentLoader
from langchain_community.document_loaders import PyPDFLoader

class PDFLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        loader = PyPDFLoader(file_path)
        return loader.load()