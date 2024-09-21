import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.storage.storage_manager import GoogleCloudStorageManager
from src.processor.text_processor import TextProcessor
from src.factory.loader_factory import DocumentLoaderFactory


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'

bucket_name = 'bucket_alexandre_teste'
storage_client = GoogleCloudStorageManager(bucket_name)


files_to_download = storage_client.list_files_in_bucket()
list_file_path = storage_client.download_files(files_to_download)
text_processor = TextProcessor()


for file_path in list_file_path:

    metadata = storage_client.file_metadata(os.path.basename(file_path))

    loader = DocumentLoaderFactory.get_loader(file_path)
    content = loader.load(file_path)

    # print(content[0].page_content)

    chunks = text_processor.chunk_documents(content[0].page_content)
    chunk_embeddings = text_processor.generate_embeddings(chunks, metadata)
    print(chunk_embeddings)

