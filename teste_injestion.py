import os
import vertexai
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_community import BigQueryVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_vertexai import VertexAI
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'service_account.json'

PROJECT_ID = os.environ.get('PROJECT')
REGION = os.environ.get('REGION')
DATASET = os.environ.get('DATASET')
TABLE = os.environ.get('TABLE')
MODEL = os.getenv('MODEL')
TEMPERATURE = os.getenv('TEMPERATURE')
MAX_OUTPUT_TOKENS = os.getenv('MAX_OUTPUT_TOKENS')
TOP_P = os.getenv('TOP_P')


vertexai.init(project=PROJECT_ID, location=REGION)
llm = VertexAI(model_name=MODEL,max_output_tokens=MAX_OUTPUT_TOKENS,temperature=TEMPERATURE, top_p=TOP_P)

embeddings_model = VertexAIEmbeddings(model_name="text-embedding-004")

# Criação do vetor store utilizando a classe nativa
vector_store = BigQueryVectorStore(
    project_id=PROJECT_ID,
    dataset_name=DATASET,
    table_name=TABLE,
    location=REGION,
    embedding=embeddings_model
)

def ingest_vectors(url, context, truncate_all=False):
    # Carrega o documento da URL
    loader = WebBaseLoader(url)
    docs = loader.load()

    # Divide o documento em partes menores
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    metadata = [{"length": len(d.page_content), "context": context} for d in documents]

    # Adiciona os textos ao BigQuery Vector Store
    vector_store.add_texts(metadatas=metadata, texts=[d.page_content for d in documents])



def search(query):

    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = BigQueryRetriever(vector_store=vector_store)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": query})
    return response['answer']



def ingest():
    ingest_vectors(context="langsmith_pricing", url="https://docs.smith.langchain.com/pricing", truncate_all=True)
    # ingest_vectors(context="cloud_workstations",
    #                url="https://practical-gcp.dev/scaling-development-teams-with-cloud-workstations/")
    # ingest_vectors(context="bigframes",
    #                url="https://practical-gcp.dev/serverless-distributed-processing-with-bigframes/")
    # ingest_vectors(context="dataplex",
    #                url="https://practical-gcp.dev/automated-data-profiling-and-quality-scan-via-dataplex/")

ingest()


# answer = search(query="how much free trace i get one the plus package with langsmith", filter={"context": "langsmith_pricing"})
# print(answer)
