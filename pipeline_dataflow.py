import os

import apache_beam as beam
from dotenv import load_dotenv
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.bigquery import WriteToBigQuery, BigQueryDisposition

from src.factory.loader_factory import DocumentLoaderFactory
from src.processor.text_processor import TextProcessor
from src.utils.config import gcs_temp_location, schema
from src.utils.storage_operator import download_blob, file_metadata, list_files_in_bucket


class DownloadAndLoadContent(beam.DoFn):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def process(self, file_path):

        local_file_path = download_blob(self.bucket_name, file_path)

        metadata = file_metadata(self.bucket_name, file_path)

        loader = DocumentLoaderFactory.get_loader(local_file_path)
        content = loader.load(local_file_path)

        yield (content, metadata)


class ChunkAndEmbedding(beam.DoFn):
    def __init__(self):
        self.text_processor = None

    def start_bundle(self):# Instância o objeto uma vez por worker
        self.text_processor = TextProcessor()  

    def process(self, content_metadata):
        content, metadata = content_metadata

        chunks = self.text_processor.chunk_documents(content[0].page_content)
        document_info = self.text_processor.generate_embeddings(chunks, metadata)

        for doc in document_info:
            yield doc


def run_pipeline(bucket_name, project_id, dataset_id, table_id):
    options = PipelineOptions(runner="DirectRunner")

    with beam.Pipeline(options=options) as pipeline:
        # storage_manager = GoogleCloudStorageManagerDataflow(bucket_name)
        file_paths = list_files_in_bucket(bucket_name)

        (
            pipeline 
            | "CreateFileList" >> beam.Create(file_paths)
            | "DownloadAndLoadContent" >> beam.ParDo(DownloadAndLoadContent(bucket_name))
            | "ChunkAndEmbedding" >> beam.ParDo(ChunkAndEmbedding())
            | "WriteToBigQuery" >> WriteToBigQuery(
                table=f'{project_id}.{dataset_id}.{table_id}',
                schema=schema,
                write_disposition=BigQueryDisposition.WRITE_APPEND,
                custom_gcs_temp_location=gcs_temp_location
                )
        )

if __name__ == "__main__":

    load_dotenv()
    bucket_name = os.getenv('BUCKET_NAME')
    project_id = os.getenv('PROJECT_ID')
    dataset_id = os.getenv('DATASET_ID')
    table_id = os.getenv('TABLE_ID')
    google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    run_pipeline(bucket_name, project_id, dataset_id, table_id)
