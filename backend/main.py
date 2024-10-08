from fastapi import FastAPI
import vertexai
from langchain_google_vertexai import VertexAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_community import BigQueryVectorStore
from controllers.similarity_controller import SimilaritySearchController
from services.similarity_service import SimilarityService
from handlers.local_file_handler import LocalFileHandler
import os



app = FastAPI()
PROJECT_ID = os.getenv('PROJECT_ID')
REGION = os.getenv('REGION')
DATASET = os.getenv('DATASET')
TABLE = os.getenv('TABLE')
MODEL = os.getenv('MODEL')
MAX_OUTPUT_TOKENS = os.getenv('MAX_OUTPUT_TOKENS')
TEMPERATURE = os.getenv('TEMPERATURE')
TOP_P = os.getenv('TOP_P')


vertexai.init(project=PROJECT_ID, location=REGION)
llm_client = VertexAI(model_name=MODEL,max_output_tokens=MAX_OUTPUT_TOKENS,temperature=TEMPERATURE, top_p=TOP_P)

embeddings_model = VertexAIEmbeddings(model_name="text-embedding-004")

vector_store = BigQueryVectorStore(
    project_id=PROJECT_ID,
    dataset_name=DATASET,
    table_name=TABLE,
    location=REGION,
    embedding=embeddings_model
)


file_handler = LocalFileHandler()

similarity_service = SimilarityService(vector_store=vector_store, llm_client=llm_client, file_handler=file_handler)

similarity_controller = SimilaritySearchController(similarity_service=similarity_service)

app.include_router(similarity_controller.router)





@app.get("/")
def read_root():
    return {"message": "Teste API"}