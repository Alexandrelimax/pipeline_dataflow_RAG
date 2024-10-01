from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
import re

class ScopeExtractor:
    def __init__(self, keywords: List[str]):
        self.keywords = keywords
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def extract_scope_chunks(self, document_text: str) -> List[str]:
        # Divida o texto em chunks
        chunks = self.text_splitter.split_text(document_text)
        
        scope_chunks = []

        # Verifique cada chunk para palavras-chave
        for chunk in chunks:
            if self.contains_scope_keywords(chunk):
                scope_chunks.append(chunk)

        return scope_chunks

    def contains_scope_keywords(self, text: str) -> bool:
        # Construa um padrão regex para verificar as palavras-chave
        pattern = re.compile(r'\b(' + '|'.join(self.keywords) + r')\b', re.IGNORECASE)
        return bool(pattern.search(text))


# Exemplo de uso
document_text = """
Apresentação
Essa proposta técnica apresenta...

Escopo do Projeto
Nesta seção, detalharemos o que será feito. 
Serão realizadas diversas atividades.

Resultados Esperados
Ao final, esperamos que...
"""

# Defina suas palavras-chave
keywords = ["escopo", "escopo do projeto", "objetivos", "o que será feito"]

scope_extractor = ScopeExtractor(keywords)
scope_chunks = scope_extractor.extract_scope_chunks(document_text)

# Agora você pode embedar os chunks encontrados
for chunk in scope_chunks:
    print("Chunk com escopo:", chunk)
    # Aqui você poderia chamar a função de embedding para cada chunk
