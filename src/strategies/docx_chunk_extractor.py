from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader


class DocxChunkExtractor:
    def __init__(self, chunk_size=300, chunk_overlap=50):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    def extract_chunks_from_document(self, file_path, start_chunk=4, end_chunk=10):
        loader = Docx2txtLoader(file_path)
        document_text = " ".join([doc.page_content for doc in loader.load()])

        chunks = self.text_splitter.split_text(document_text)

        # Limpa os chunks e retorna apenas o intervalo relevante
        cleaned_chunks = [self.clean_chunk(chunk) for chunk in chunks[start_chunk:end_chunk]]
        return cleaned_chunks


    def clean_chunk(self, chunk: str) -> str:
        return ' '.join(chunk.strip().split())