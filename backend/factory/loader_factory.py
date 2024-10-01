from src.interfaces.document_loader import DocumentLoader
from src.strategies.docx_document import DocxLoader
from src.strategies.pdf_document import PDFLoader


class DocumentLoaderFactory:
    loaders = {
        '.pdf': PDFLoader,
        '.docx': DocxLoader
    }

    @staticmethod
    def get_loader(file_path: str) -> DocumentLoader:
        for ext, loader in DocumentLoaderFactory.loaders.items():
            if file_path.endswith(ext):
                return loader()

        raise ValueError(f"Tipo de arquivo '{file_path}' não suportado.")
