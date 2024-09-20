from factory import DocumentLoaderFactory
from google.cloud import storage, bigquery
from download_file import download_files_to_temp

def list_files_in_bucket(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    
    return [blob for blob in blobs if blob.name.endswith('.pdf') or blob.name.endswith('.docx')]

bucket_name = 'alexandre-bucket-teste'
files_to_download = list_files_in_bucket(bucket_name)
files_directory = download_files_to_temp(bucket_name, files_to_download)

print(files_directory)
for file in files_directory:

    loader = DocumentLoaderFactory.get_loader(file)
    print(file)
    text = loader.load(file)
    print(text)

