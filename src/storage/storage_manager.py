import os
from google.cloud import storage
from google.cloud.storage import Blob
from typing import List, Dict

class GoogleCloudStorageManager:
    def __init__(self, bucket_name, temp_folder="/tmp"):
        self.bucket_name = bucket_name
        self.temp_folder = temp_folder
        self.client = storage.Client()
        self.create_temp_folder()

    def create_temp_folder(self) -> None:
        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)
            print(f"Pasta temporária criada: {self.temp_folder}")

    def download_blob(self, source_blob_name, destination_file_name) -> None:
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print(f"Arquivo {source_blob_name} baixado para {destination_file_name}.")

    def download_files(self, files_to_download: List[Blob]) -> List[str]:
        downloaded_files = []

        for blob in files_to_download:
            file_name = blob.name
            local_file_path = os.path.join(self.temp_folder, file_name.replace("/", "_"))

            self.download_blob(file_name, local_file_path)

            downloaded_files.append(local_file_path)

        return downloaded_files
    
    def list_files_in_bucket(self) -> List[Blob]:
        bucket = self.client.bucket(self.bucket_name)
        blobs = bucket.list_blobs()

        filtered_files = [blob for blob in blobs if blob.name.endswith('.pdf') or blob.name.endswith('.docx')]
        return filtered_files


    def file_metadata(self, file_name: str) -> Dict[str, str]:
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.get_blob(file_name)

        if blob:
            metadata = {
                'file_name': blob.name,
                'mime_type': blob.content_type,
                'gs_uri': f'gs://{self.bucket_name}/{file_name}'
            }
            return metadata