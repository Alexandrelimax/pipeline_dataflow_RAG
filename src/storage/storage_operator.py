from google.cloud import storage
from typing import List, Dict
import os


def create_temp_folder(temp_folder: str = "/tmp") -> None:
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
        print(f"Pasta temporária criada: {temp_folder}")

def list_files_in_bucket(bucket_name) -> List[str]:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blobs = bucket.list_blobs()

        filtered_files = [f'gs://{bucket_name}/{blob.name}' for blob in blobs if blob.name.endswith('.pdf') or blob.name.endswith('.docx')]
        return filtered_files


def download_blob(bucket_name: str, file_path: str, temp_folder: str = "/tmp") -> str:
    client = storage.Client()
    create_temp_folder(temp_folder)

    # Extrai o nome do arquivo
    file_name = file_path.split('/')[-1]
    bucket = client.bucket(bucket_name)

    # Cria o blob usando o caminho relativo
    blob = bucket.blob(file_path.replace(f'gs://{bucket_name}/', ''))

    local_file_path = os.path.join(temp_folder, file_name.replace("/", "_"))
    blob.download_to_filename(local_file_path)

    print(f"Arquivo {file_name} baixado para {local_file_path}.")
    return local_file_path


def file_metadata(bucket_name: str, file_path: str) -> Dict[str, str]:
    file_name = file_path.split('/')[-1]
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.get_blob(file_name)

    if blob:
        metadata = {
            'file_name': blob.name,
            'mime_type': blob.content_type,
            'gs_uri': file_path
        }
        return metadata
    return {}
