from google.cloud import storage, bigquery
from datetime import datetime
from strategies.context import DocumentLoaderFactory
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'



# Função para consultar documentos já processados no BigQuery
def get_processed_documents():
    client = bigquery.Client()
    
    # Consulta para pegar todos os documentos processados
    query = """
        SELECT document_name
        FROM `seu_projeto.sua_dataset.seu_tabela_processamento`
    """
    
    query_job = client.query(query)  # Executa a consulta
    
    processed_documents = [row.document_name for row in query_job]  # Extrai os nomes dos documentos
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


def extract_text_from_file(file_path):
    # Implementar a lógica para extrair texto do PDF ou DOCX
    return "Texto extraído do arquivo: {}".format(file_path)  # Simulação


def extract_blob_metadata(blob):
    return {
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "updated": blob.updated.isoformat()
    }
# def generate_embeddings(chunks):
#     embedding_model = VertexAIEmbeddings()  # Vertex AI Embeddings
#     embeddings = []
#     for chunk in chunks:
#         embedding = embedding_model.embed(chunk)
#         embeddings.append({
#             'chunk_text': chunk,
#             'embedding': embedding
#         })
#     return embeddings

# Função para processar novos arquivos
def process_new_files(bucket_name):
    processed_documents = get_processed_documents()
    
    bucket_files = list_files_in_bucket(bucket_name)
    new_files = filter_new_files(bucket_files, processed_documents)
    
    if not new_files:
        print("Nenhum novo documento para processar.")
        return
    
    # Inicializa o modelo de embeddings
    embeddings = VertexAIEmbeddings(model_name=MODEL_NAME)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)

    for blob in new_files:
        print(f"Processando arquivo: {blob.name}")

        # Obtém o carregador apropriado
        loader = DocumentLoaderFactory.get_loader(blob.name)
        
        # Extrai o texto do arquivo
        text = loader.load(blob.name)
        
        # Cria chunks do texto
        documents = text_splitter.split_text(text)
        docs = [Document(page_content=doc) for doc in documents]
        
        # Gera embeddings para os chunks
        embedding_vectors = embeddings.embed_documents(docs)

        # Cria uma lista de dicionários para cada chunk e seu embedding
        data_to_save = []
        for doc, embedding in zip(documents, embedding_vectors):
            data_to_save.append({
                "document_name": blob.name,
                "chunk": doc,
                "embedding": json.dumps(embedding),
                **extract_blob_metadata(blob)
            })

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
