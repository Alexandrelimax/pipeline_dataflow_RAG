import os
from google.cloud import storage

# Função para criar a pasta temporária
def create_temp_folder(temp_folder):
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
        print(f"Pasta temporária criada: {temp_folder}")


def download_files_to_temp(bucket_name, files_to_download, temp_folder="/tmp"):
    """Recebe uma lista de arquivos e baixa todos para uma pasta temporária."""
    
    # Cria a pasta temporária, se ainda não existir
    create_temp_folder(temp_folder)
    
    downloaded_files = []
    
    # Baixa cada arquivo da lista para a pasta temporária
    for blob in files_to_download:
        # Define o caminho local do arquivo na pasta temporária
        file_name = blob.name
        local_file_path = os.path.join(temp_folder, file_name.replace("/", "_"))  # Substitui '/' por '_'
        
        # Baixa o arquivo do bucket
        download_blob(bucket_name, file_name, local_file_path)
        
        # Adiciona o caminho do arquivo baixado à lista de arquivos baixados
        downloaded_files.append(local_file_path)
    
    return downloaded_files  # Retorna a lista dos caminhos locais dos arquivos baixados

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Baixa um blob do bucket para uma pasta temporária."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    
    blob.download_to_filename(destination_file_name)
    print(f"Arquivo {source_blob_name} baixado para {destination_file_name}.")
