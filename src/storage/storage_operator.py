from google.cloud import storage
from typing import List, Dict
import os
import tempfile

def create_temp_folder() -> str:
    temp_folder = tempfile.mkdtemp()
    return temp_folder

def list_files_in_bucket(bucket_name) -> List[str]:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blobs = bucket.list_blobs()
        filtered_files = [f'gs://{bucket_name}/{blob.name}' for blob in blobs if blob.name.endswith('.pdf') or blob.name.endswith('.docx')]
        return filtered_files


def download_blob(bucket_name: str, file_path: str) -> str:
    client = storage.Client()
    temp_folder = create_temp_folder()  # Cria a pasta temporária

    file_name = os.path.basename(file_path)
    bucket = client.bucket(bucket_name)

    blob = bucket.get_blob(file_path.replace(f'gs://{bucket_name}/', ''))

    local_file_path = os.path.join(temp_folder, file_name)
    blob.download_to_filename(local_file_path)

    return local_file_path



def file_metadata(bucket_name: str, file_path: str) -> Dict[str, str]:
    client = storage.Client()
    relative_path = file_path.replace(f'gs://{bucket_name}/', '')
    bucket = client.bucket(bucket_name)
    blob = bucket.get_blob(relative_path)

    if blob.exists():
        metadata = {
            'file_name': os.path.basename(file_path),
            'mime_type': blob.content_type,
            'gs_uri': file_path
        }
        return metadata
    return {}


