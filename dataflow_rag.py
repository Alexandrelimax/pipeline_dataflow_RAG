import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import storage
from google.cloud import bigquery
from langchain.embeddings import VertexAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime

# Função para extrair metadados do arquivo
def get_essential_metadata(bucket_name, file_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.get_blob(file_name)

    if blob:
        metadata = {
            'file_name': blob.name,
            'mime_type': blob.content_type,
            'gs_uri': f'gs://{bucket_name}/{file_name}',

        }
        return metadata
    else:
        raise FileNotFoundError(f"Arquivo {file_name} não encontrado no bucket {bucket_name}")

# Função para fazer o chunking do conteúdo do documento
def chunk_text(document_content):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_text(document_content)

# Função para gerar embeddings para os chunks
def generate_embeddings(chunks):
    embedding_model = VertexAIEmbeddings()  # Vertex AI Embeddings
    embeddings = []
    for chunk in chunks:
        embedding = embedding_model.embed(chunk)
        embeddings.append({
            'chunk_text': chunk,
            'embedding': embedding
        })
    return embeddings

# Função para escrever no BigQuery
def write_to_bigquery(metadata, chunk_embeddings, table_id):
    client = bigquery.Client()

    # Construir as linhas para inserção no BigQuery
    rows_to_insert = [
        {
            "file_name": metadata["file_name"],
            "mime_type": metadata["mime_type"],
            "gs_uri": metadata["gs_uri"],
            "signed_url": metadata["signed_url"],
            "chunk_text": chunk_embedding['chunk_text'],
            "embedding": chunk_embedding['embedding'],
        }
        for chunk_embedding in chunk_embeddings
    ]

    # Inserir no BigQuery
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        raise RuntimeError(f"Erro ao inserir dados no BigQuery: {errors}")

# Função para registrar o documento processado
def log_processed_document(metadata, log_table):
    client = bigquery.Client()
    row = {
        "file_name": metadata["file_name"],
        "gs_uri": metadata["gs_uri"],
        "processed_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }
    errors = client.insert_rows_json(log_table, [row])
    if errors:
        raise RuntimeError(f"Erro ao registrar log no BigQuery: {errors}")

# Função para verificar se o documento já foi processado
def is_document_already_processed(file_name, log_table):
    client = bigquery.Client()

    query = f"""
    SELECT file_name FROM `{log_table}`
    WHERE file_name = '{file_name}'
    """
    query_job = client.query(query)

    return query_job.result().total_rows > 0

# Função para processar um documento
def process_document(bucket_name, file_name, embeddings_table, log_table):
    # Extrair metadados
    metadata = get_essential_metadata(bucket_name, file_name)

    # Baixar conteúdo do documento
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.get_blob(file_name)
    document_content = blob.download_as_text()

    # Fazer chunking do texto
    chunks = chunk_text(document_content)

    # Gerar embeddings para cada chunk e manter a correspondência
    chunk_embeddings = generate_embeddings(chunks)

    # Escrever os dados no BigQuery
    write_to_bigquery(metadata, chunk_embeddings, embeddings_table)

    # Registrar documento processado
    log_processed_document(metadata, log_table)

# Função para listar arquivos no bucket
def list_files_in_bucket(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()
    return [blob.name for blob in blobs]

# Função para filtrar arquivos novos
def filter_new_files(file_name, log_table):
    client = bigquery.Client()

    query = f"""
    SELECT file_name FROM `{log_table}`
    WHERE file_name = '{file_name}'
    """
    query_job = client.query(query)

    return query_job.result().total_rows == 0

# Função principal do pipeline
def run_pipeline(bucket_name, embeddings_table, log_table):
    # Define opções do pipeline do Apache Beam
    options = PipelineOptions()

    with beam.Pipeline(options=options) as p:
        # Listar arquivos no bucket
        file_names = p | "Listar Arquivos no Bucket" >> beam.Create(list_files_in_bucket(bucket_name)))

        # Filtrar arquivos novos
        new_files = file_names | "Filtrar Arquivos Novos" >> beam.Filter(lambda file_name: filter_new_files(file_name, log_table))

        # Processar documentos novos
        new_files | "Processar Documento" >> beam.Map(lambda file_name: process_document(bucket_name, file_name, embeddings_table, log_table))

if __name__ == "__main__":
    # Nome do bucket, tabela de embeddings e tabela de log do BigQuery
    bucket_name = 'bucket_alexandre_teste'
    embeddings_table = 'projeto_dataset.embeddings_table'
    log_table = 'projeto_dataset.processed_documents'

    # Executar o pipeline
    run_pipeline(bucket_name, embeddings_table, log_table)
