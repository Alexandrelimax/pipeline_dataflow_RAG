from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class PDFChunkExtractor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def extract_chunks_from_document(self, file_path, start_chunk=4, end_chunk=10):
        # Carrega o documento PDF
        loader = PyPDFLoader(file_path)
        document_text = " ".join([doc.page_content for doc in loader.load()])  # Junta o texto das páginas

        # Divide o texto em chunks
        chunks = self.text_splitter.split_text(document_text)
        cleaned_chunks = [self.clean_chunk(chunk) for chunk in chunks[start_chunk:end_chunk]]
        
        return cleaned_chunks

    def clean_chunk(self, chunk):
        return ' '.join(chunk.strip().split())