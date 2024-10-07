from typing import List, Any
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class BigQueryRetriever(BaseRetriever):
    vector_store: Any
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vector_store =  kwargs.get('vector_store')


    def get_relevant_documents(self, query: str) -> List[Document]:
        return self.vector_store.similarity_search(query=query)
