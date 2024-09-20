from langchain.document_loaders import  DocxLoader
from interface import DocumentLoader

class DocxLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        loader = DocxLoader(file_path)
        return loader.load()  # Método fictício; ajuste conforme necessário