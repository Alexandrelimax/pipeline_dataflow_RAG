import os

import apache_beam as beam
from dotenv import load_dotenv
from apache_beam.options.pipeline_options import PipelineOptions
from langchain_google_community import BigQueryVectorStore
from langchain_google_vertexai import VertexAIEmbeddings

from src.factory.loader_factory import DocumentLoaderFactory
from src.strategies.docx_chunk_extractor import DocxChunkExtractor
from src.strategies.metadata_extractor import MetadataExtractor
from src.storage.storage_operator import download_blob, file_metadata, list_files_in_bucket


class DownloadFileGCS(beam.DoFn):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def process(self, file_path):
        local_file_path = download_blob(self.bucket_name, file_path)
        metadata = file_metadata(self.bucket_name, file_path)

        yield (local_file_path, metadata)


class ChunkProcessor(beam.DoFn):
    def __init__(self, project_id, dataset_name, table_name, region):
            self.vector_store = None
            self.embedding_model = None
            self.project_id = project_id
            self.dataset_name = dataset_name
            self.table_name = table_name
            self.region = region

    def start_bundle(self):
        self.embedding_model = VertexAIEmbeddings(model_name="text-embedding-004")
        self.vector_store = BigQueryVectorStore(
            project_id=self.project_id,
            dataset_name=self.dataset_name,
            table_name=self.table_name,
            location=self.region,
            embedding=self.embedding_model
        )

    def process(self, content_metadata):
        local_file_path, metadata = content_metadata
        loader = DocumentLoaderFactory.get_loader(local_file_path)

        try:
            chunks = loader.extract_chunks_from_document(local_file_path)
            metadatas = [MetadataExtractor.extract_metadata(index, metadata) for index, _ in enumerate(chunks)]

            # print(chunks)
            self.vector_store.add_texts(metadatas=metadatas, texts=chunks)
            yield f"Processado {metadata.get('file_name')}"
        except Exception as e:
            yield f"Erro ao processar {metadata.get('file_name')}: {e}"





def run_pipeline(bucket_name, project, dataset, table, region):
    options = PipelineOptions(runner="DirectRunner")

    with beam.Pipeline(options=options) as pipeline:
        file_paths = list_files_in_bucket(bucket_name)

        (
            pipeline 
            | "ListFilesInBucket" >> beam.Create(file_paths)
            | "DownloadAndExtractMetadata" >> beam.ParDo(DownloadFileGCS(bucket_name))
            | "ProcessChunksAndStoreEmbeddings" >> beam.ParDo(ChunkProcessor(project, dataset, table, region))
        )

if __name__ == "__main__":

    load_dotenv()
    project = os.environ.get('PROJECT')
    region = os.environ.get('REGION')
    dataset = os.environ.get('DATASET')
    table = os.environ.get('TABLE')
    bucket_name = os.environ.get('BUCKET_NAME')
    google_credentials = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    run_pipeline(bucket_name, project, dataset, table, region)
