from typing import Any
from interfaces.similarity_interface import ISimilarity
from factory.loader_factory import DocumentLoaderFactory
from core.prompts.prompt_retriever import prompt
from core.retrievers.bigquery_retriever import BigQueryRetriever
from interfaces.file_handler_interface import FileHandlerInterface
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain




class SimilarityService(ISimilarity):
    def __init__(self, vector_store, llm_client, file_handler: FileHandlerInterface):
        self.llm_client = llm_client
        self.file_handler = file_handler
        self.retriever = BigQueryRetriever(vector_store=vector_store)


    async def process_document(self, document_data: bytes, file_name: str) -> Any:

        temp_file_path = f"/tmp/{file_name}"
        try:
            self.file_handler.write(temp_file_path, document_data)
            loader = DocumentLoaderFactory.get_loader(temp_file_path)
            chunks = loader.extract_chunks_from_document(temp_file_path, start_chunk=4, end_chunk=8)




        except ValueError as e:
            raise ValueError(f"Erro ao carregar o documento: {e}")
        finally:
            self.file_handler.remove(temp_file_path)

        return await self.perform_similarity_search(document_text)
        


    async def process_text(self, text: str) -> Any:
        #Realiza a busca por similaridade com base no texto fornecido.
        document_chain = create_stuff_documents_chain(self.llm_client, prompt)
        retrieval_chain = create_retrieval_chain(self.retriever, document_chain)
        response = retrieval_chain.invoke({"input": text})
        return response['answer']
