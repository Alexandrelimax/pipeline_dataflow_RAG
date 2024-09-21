import pandas as pd
from typing import List, Dict, Any
from google.cloud import bigquery 
from google.cloud.bigquery import LoadJobConfig, WriteDisposition
from src.interfaces.vector_database import VectorDatabase

class BigQueryVectorDatabase(VectorDatabase):
    def __init__(self, project_id: str, dataset_id: str, table_id: str) -> None:
        self.client = bigquery.Client(project=project_id)
        self.dataset_id = dataset_id
        self.table_id = table_id

    def create_table(self) -> None:

        schema = [
            bigquery.SchemaField("uuid", "STRING"),
            bigquery.SchemaField("embeddings", "ARRAY<FLOAT64>"),
            bigquery.SchemaField("content", "STRING"),
            bigquery.SchemaField("chunk_number", "INT64"),
            bigquery.SchemaField("file_name", "STRING"),
            bigquery.SchemaField("mime_type", "STRING"),
            bigquery.SchemaField("gs_uri", "STRING"),
        ]
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        table = bigquery.Table(table_ref, schema=schema)
        self.client.create_table(table, exists_ok=True)

    def save_embeddings(self, embeddings: List[Dict[str, Any]]) -> None:

        df = pd.DataFrame(embeddings)

        table_ref = f"{self.dataset_id}.{self.table_id}"
        job_config = LoadJobConfig(
            write_disposition=WriteDisposition.WRITE_APPEND,
        )

        job = self.client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()

        print(f"Dados carregados para {table_ref} com sucesso.")


    def search(self, query_embedding: List[float], top_k: int) -> List[Dict[str, Any]]:

        pass
