import os

from interfaces.document_loader import DocumentLoader
from strategies.pdf_chunk_extractor import PDFChunkExtractor
from strategies.docx_chunk_extractor import DocxChunkExtractor

class DocumentLoaderFactory:
    loaders = {
        '.pdf': PDFChunkExtractor,
        '.docx': DocxChunkExtractor
    }

    @staticmethod
    def get_loader(file_path: str) -> DocumentLoader:
        _, ext = os.path.splitext(file_path.lower())

        if ext in DocumentLoaderFactory.loaders:
            return DocumentLoaderFactory.loaders[ext]()
        
        raise ValueError(f"Tipo de arquivo '{file_path}' não suportado.")


    # @staticmethod
    # def get_loader(file_path: str) -> DocumentLoader:
    #     for ext, loader in DocumentLoaderFactory.loaders.items():
    #         if file_path.endswith(ext):
    #             return loader()

    #     raise ValueError(f"Tipo de arquivo '{file_path}' não suportado.")