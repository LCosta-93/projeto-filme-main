import chromadb
from chromadb.config import Settings
#from chromadb.client import Client

import json
import os

persist_dir = "../dados/chroma_storage"
if not os.path.exists(persist_dir):
    os.makedirs(persist_dir)  # Cria o diretório, se não existir

# Configuração do ChromaDB
#settings = Settings(
#    persist_directory=persist_dir
#)
#client = chromadb.Client(settings)

client = chromadb.PersistentClient(path=persist_dir)

# Crie ou obtenha a coleção
collection_name = "filmes_collection"
collection = client.get_or_create_collection(name=collection_name)
#collection = client.create_collection(name=collection_name)


# Carregar dados do arquivo JSON
try:
    with open("filmes.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
except FileNotFoundError:
    print("Arquivo 'filmes.json' não encontrado. Certifique-se de que ele está na pasta correta.")
    dados = []

# Importar os dados para a coleção
for item in dados:
    print(item["Title"])
    try:
        collection.add(
            documents=[item["Title"]],
            metadatas={"Filme": item["Title"], "Ano": item["Year"]},  # Adicione metadados
            ids=[str(item["id"])]  # Identificadores únicos
        )
    except Exception as e:
        print(f"Erro ao adicionar o item {item['Title']}: {e}")


num_registros = collection.count()
print(f"Quantidade de registros na coleção '{collection_name}': {num_registros}")


results = collection.query(
    query_texts=["Quais filmes de 1982"], # Chroma will embed this for you
    n_results=3 # how many results to return
)

print(results)
