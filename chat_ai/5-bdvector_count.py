import chromadb
from chromadb.config import Settings
#from chromadb.client import Client

import json
import os

persist_dir = "../dados/chroma_storage"
if not os.path.exists(persist_dir):
    os.makedirs(persist_dir)

# Configuração do ChromaDB
settings = Settings(
    persist_directory=persist_dir
)

client = chromadb.PersistentClient(path=persist_dir)


# Listar todas as coleções disponíveis
colecoes = client.list_collections()

# Crie ou obtenha a coleção
collection_name = "filmes_collection"
collection = client.get_collection(name=collection_name)

num_registros = collection.count()
print(f"Quantidade de registros na coleção '{collection_name}': {num_registros}")
