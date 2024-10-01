from langchain_community.document_loaders import Docx2txtLoader
from interfaces.document_loader import DocumentLoader

class DocxLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        loader = Docx2txtLoader(file_path)
        return loader.load()
    