
from src.strategies.docx_chunk_extractor import DocxChunkExtractor
from src.strategies.pdf_chunk_extractor import PDFChunkExtractor


class DocumentLoaderFactory:
    loaders = {
        '.pdf': PDFChunkExtractor,
        '.docx': DocxChunkExtractor
    }

    @staticmethod
    def get_loader(file_path: str):
        for ext, loader in DocumentLoaderFactory.loaders.items():
            if file_path.endswith(ext):
                return loader()

        raise ValueError(f"Tipo de arquivo '{file_path}' não suportado.")
