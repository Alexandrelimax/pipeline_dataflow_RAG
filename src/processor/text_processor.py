from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings
from src.utils.generate_id import generate_uuid
from typing import List, Dict, Any

class TextProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embedding_model = VertexAIEmbeddings(model_name="text-embedding-004")

    def chunk_documents(self, document: str) -> List[str]:
        return self.text_splitter.split_text(document)

    def generate_embeddings(self, chunks: List[str], metadata: Dict[str, str]) -> List[Dict[str, Any]]:
        document_info = []
        for i, chunk in enumerate(chunks):
            embedding = self.embedding_model.embed_query(chunk)
            document_info.append({
                'uuid': generate_uuid(),
                'embeddings': embedding,
                'content': chunk,
                'chunk_number': i,
                'file_name': metadata.get('file_name', ''),
                'mime_type': metadata.get('mime_type', ''),
                'gs_uri': metadata.get('gs_uri', '')
            })
        return document_info
