from interface import DocumentLoader
from docx_document import DocxLoader
from pdf_document import PDFLoader


class DocumentLoaderFactory:
    @staticmethod
    def get_loader(file_path: str) -> DocumentLoader:
        if file_path.endswith('.pdf'):
            return PDFLoader()
        elif file_path.endswith('.docx'):
            return DocxLoader()
        else:
            raise ValueError("Tipo de arquivo não suportado.")