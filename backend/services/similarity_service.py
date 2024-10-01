from interfaces.similarity_interface import ISimilarity
from factory.loader_factory import DocumentLoaderFactory
from repositories.vector_repository import VectorRepository
from interfaces.file_handler_interface import FileHandlerInterface
from typing import Any

class SimilarityService(ISimilarity):
    def __init__(self, vector_repository: VectorRepository, file_handler: FileHandlerInterface):
        self.vector_repository = vector_repository
        self.file_handler = file_handler

    async def process_document(self, document_data: bytes, file_name: str) -> Any:

        temp_file_path = f"/tmp/{file_name}"
        try:
            self.file_handler.write(temp_file_path, document_data)
            loader = DocumentLoaderFactory.get_loader(temp_file_path)
            document_text = loader.load(temp_file_path)
        except ValueError as e:
            raise ValueError(f"Erro ao carregar o documento: {e}")
        finally:
            self.file_handler.remove(temp_file_path)

        






        return await self.perform_similarity_search(document_text)

    async def process_text(self, text: str) -> Any:
        """
        Processa o texto diretamente e realiza a busca por similaridade.

        Args:
            text (str): O texto a ser processado.

        Returns:
            Any: Resultado da busca por similaridade.
        """
        return await self.perform_similarity_search(text)

    async def perform_similarity_search(self, text: str) -> Any:
        """
        Realiza a busca por similaridade com base no texto fornecido.

        Args:
            text (str): O texto extraído ou fornecido.

        Returns:
            Any: Resultado da busca por similaridade.
        """
        embedding = self.generate_embedding(text)
        search_results = self.vector_repository.search_similar_documents(embedding)
        return {"similarity_results": search_results}

    def generate_embedding(self, text: str) -> list:
        """
        Gera um embedding do texto.

        Args:
            text (str): O texto a ser embeddado.

        Returns:
            list: Embedding gerado a partir do texto.
        """
        return [0.1, 0.2, 0.3]  # Substitua com a lógica real de embeddings
