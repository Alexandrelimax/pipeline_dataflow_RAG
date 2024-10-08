#%%
from langchain_google_community import GCSDirectoryLoader
from google.cloud.bigquery import Client
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

#%%
bucket_name = os.getenv('BUCKET_NAME')
project_id = os.getenv('PROJECT')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'service_account_super.json'# region = os.getenv('REGION')
dataset_id = os.getenv('DATASET')
table_id = os.getenv('TABLE')
region = os.getenv('REGION')


#%%
# loader = GCSDirectoryLoader(project_name=project_id, bucket=bucket_name)

# res = loader.load()

# res
print(dataset_id)
#%%
client = Client(project=project_id, location=region)
client.create_dataset(dataset=dataset_id, exists_ok=True)
# %%
import os
import vertexai
from langchain_google_community import BigQueryVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_vertexai import VertexAI


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'service_account.json'
# Configurações

MAX_OUTPUT_TOKENS = 1000
TEMPERATURE = 1
TOP_P = 0.95
DATASET = os.getenv('DATASET')
TABLE = os.getenv('TABLE')
PROJECT_ID = os.getenv('PROJECT')
REGION = os.getenv('REGION')
MODEL = os.getenv('MODEL')
MAX_OUTPUT_TOKENS = os.getenv('MAX_OUTPUT_TOKENS')
TEMPERATURE = os.getenv('TEMPERATURE')
TOP_P = os.getenv('TOP_P')

#%%
vertexai.init(project=PROJECT_ID, location=REGION)
llm = VertexAI(model_name=MODEL,max_output_tokens=MAX_OUTPUT_TOKENS,temperature=TEMPERATURE, top_p=TOP_P)

embeddings_model = VertexAIEmbeddings(model_name="textembedding-gecko@001")

# Criação do vetor store utilizando a classe nativa
vector_store = BigQueryVectorStore(
    project_id=PROJECT_ID,
    dataset_name=DATASET,
    table_name=TABLE,
    location=REGION,
    embedding=embeddings_model
)
# %%
