from interface import DocumentLoader
from langchain.document_loaders import PyPDFLoader

class PDFLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        loader = PyPDFLoader(file_path)
        return loader.load()  # Método fictício; ajuste conforme necessário