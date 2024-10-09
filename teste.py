#%%

import os
import vertexai
from langchain_google_community import BigQueryVectorStore
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.vectorstores.utils import DistanceStrategy

from langchain_google_vertexai import VertexAI
from dotenv import load_dotenv
load_dotenv(override=True)


# %%

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

vector_store = BigQueryVectorStore(
    project_id=PROJECT_ID,
    dataset_name=DATASET,
    table_name=TABLE,
    location=REGION,
    embedding=embeddings_model,
    distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE
)


# %%
result = vector_store.similarity_search('O objetivo principal é fornecer uma plataforma centralizada onde as', k=2)
print(result)



# %%
query = 'O objetivo principal é fornecer uma plataforma centralizada'
query_vector = embeddings_model.embed_query(query)
docs = vector_store.similarity_search_by_vector(query_vector, k=5)
print(docs)