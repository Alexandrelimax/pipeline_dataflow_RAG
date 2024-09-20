from google.cloud import storage, bigquery
from strategies.context import DocumentLoaderFactory
import os
from utils.create_temp_directory import create_temp_folder
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'
# embedding_model = VertexAIEmbeddings(model_name='text-embedding-004')
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=75)

def download_files_to_temp(bucket_name, files_to_download, temp_folder="/tmp"):
    """Recebe uma lista de arquivos e baixa todos para uma pasta temporária."""
    
    # Cria a pasta temporária, se ainda não existir
    create_temp_folder(temp_folder)
    
    downloaded_files = []
    
    # Baixa cada arquivo da lista para a pasta temporária
    for file_name in files_to_download:
        # Define o caminho local do arquivo na pasta temporária
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

def get_processed_documents():
    client = bigquery.Client()
    
    query = """
        SELECT document_name
        FROM `seu_projeto.sua_dataset.seu_tabela_processamento`
    """
    
    query_job = client.query(query)
    
    processed_documents = [row.document_name for row in query_job]
    return processed_documents

# Função para listar arquivos no bucket do Cloud Storage
def list_files_in_bucket(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    
    return [blob.name for blob in blobs if blob.name.endswith('.pdf') or blob.name.endswith('.docx')]

# Função para filtrar arquivos que não foram processados
def filter_new_files(bucket_files, processed_documents):
    # Filtra arquivos que não foram processados
    return [file for file in bucket_files if file not in processed_documents]



def extract_blob_metadata(blob):
    return {
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,

    }
def generate_embeddings(chunks, embedding_model):
    data_to_save = []
    
    for i, chunk in enumerate(chunks, start=1):
        embedding = embedding_model.embed_query(chunk)
        
        data_to_save.append({
            "chunk_number": i,
            "chunk": chunk,
            "embedding": json.dumps(embedding)
        })
    
    return data_to_save
def process_new_files(bucket_name):
    processed_documents = get_processed_documents()
    
    bucket_files = list_files_in_bucket(bucket_name)
    new_files = filter_new_files(bucket_files, processed_documents)
    
    if not new_files:
        print("Nenhum novo documento para processar.")
        return
    


    for blob in new_files:
        print(f"Processando arquivo: {blob.name}")

        
        loader = DocumentLoaderFactory.get_loader(blob.name)
        
        text = loader.load(blob.name)
        
        splited_text = text_splitter.split_text(text)
        chunks = [Document(page_content=doc) for doc in splited_text]
        
        embedding_data = generate_embeddings(chunks, embedding_model)


        data_to_save = [
            {**data, **extract_blob_metadata(blob), "document_name": blob.name}
            for data in embedding_data
        ]

        print(data_to_save)

        # Salvar dados no BigQuery
#         save_document_metadata_to_bq(data_to_save)



# # Função para salvar metadados dos documentos processados no BigQuery
# def save_document_metadata_to_bq(document_name):
#     client = bigquery.Client()
    
#     table_id = "seu_projeto.sua_dataset.seu_tabela_processamento"
#     rows_to_insert = [
#         {
#             "document_name": document_name,
#             "processing_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         }
#     ]
    
#     errors = client.insert_rows_json(table_id, rows_to_insert)  # Inserção no BQ
#     if errors:
#         print(f"Erro ao inserir dados no BigQuery: {errors}")
#     else:
#         print(f"Metadados do documento {document_name} salvos com sucesso.")

# Função principal para executar o fluxo
def main(bucket_name):
    process_new_files(bucket_name)

if __name__ == "__main__":
    bucket_name = "seu_bucket_name"  # Substitua pelo nome do seu bucket
    main(bucket_name)
