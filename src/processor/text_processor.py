from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings

class TextProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embedding_model = VertexAIEmbeddings(model_name="text-embedding-004")

    def chunk_documents(self, document):
        return  self.text_splitter.split_text(document)

    def generate_embeddings(self, chunks, metadata):
        embeddings = []
        for i, chunk in enumerate(chunks):
            embedding = self.embedding_model.embed_query(chunk)
            embeddings.append({
                'chunk': i,
                'content': chunk,
                'embeddings': embedding,
                'metadata': metadata
            })
        return embeddings

