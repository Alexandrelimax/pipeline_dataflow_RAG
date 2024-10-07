from fastapi import FastAPI
import vertexai
from langchain_google_vertexai import VertexAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_community import BigQueryVectorStore
from controllers.similarity_controller import SimilaritySearchController
from services.similarity_service import SimilarityService
from handlers.local_file_handler import LocalFileHandler

app = FastAPI()
PROJECT_ID = ''
REGION = 'us-central1'
DATASET = "vector_store"
TABLE = "doc_and_vectors"

MODEL = 'gemini-1.5-flash'
MAX_OUTPUT_TOKENS = 1000
TEMPERATURE = 1
TOP_P = 0.95


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