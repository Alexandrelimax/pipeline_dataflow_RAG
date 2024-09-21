import os
from dotenv import load_dotenv

from src.storage.storage_manager import GoogleCloudStorageManager
from src.processor.text_processor import TextProcessor
from src.factory.loader_factory import DocumentLoaderFactory
from src.database.bigquery_vectordb import BigQueryVectorDatabase
load_dotenv()


project_id = os.getenv('PROJECT_ID')
dataset_id = os.getenv('DATASET_ID')
table_id = os.getenv('TABLE_ID')
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
bucket_name = os.getenv('BUCKET_NAME')


storage_client = GoogleCloudStorageManager(bucket_name)
bigquery_db = BigQueryVectorDatabase(project_id=project_id, dataset_id=dataset_id, table_id=table_id)

files_to_download = storage_client.list_files_in_bucket()
list_file_path = storage_client.download_files(files_to_download)
text_processor = TextProcessor()

for file_path in list_file_path:

    metadata = storage_client.file_metadata(os.path.basename(file_path))

    loader = DocumentLoaderFactory.get_loader(file_path)
    content = loader.load(file_path)

    chunks = text_processor.chunk_documents(content[0].page_content)
    chunk_embeddings = text_processor.generate_embeddings(chunks, metadata)

    bigquery_db.save_embeddings(chunk_embeddings)


