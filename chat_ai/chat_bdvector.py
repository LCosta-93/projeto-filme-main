from dotenv import load_dotenv
load_dotenv()

import streamlit as st

import chromadb
from chromadb.config import Settings
import json


def json_to_collection(collection):
    # Carregar dados do arquivo JSON
    with open("filmes.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Importar os dados para a coleção
    for item in dados:
        collection.add(
            documents=[f'O filme {item["Title"]} foi lançado no ano {item["Year"]}'],
            metadatas={"Filme": item["Title"], "Ano": item["Year"]},  # Adicione metadados
            ids=[str(item["id"])]  # Identificadores únicos
        )
    return collection

def get_collection(collection_name):
    # Configuração do ChromaDB
    client = chromadb.Client(Settings(
        persist_directory="./chroma_storage"  # Diretório para persistir dados
    ))

    # Listar todas as coleções disponíveis
    colecoes = client.list_collections()

    # Verificar se "minha_collection" existe
    if any(colecao.name == collection_name for colecao in colecoes):
        collection = client.get_collection(name=collection_name)
    else:
        # Crie ou obtenha a coleção
        collection = client.create_collection(name=collection_name)
        collection = json_to_collection(collection)

    return collection

def get_response2(collection_name, query_texts):
    collection = get_collection(collection_name)
    results = collection.query(
        query_texts=query_texts,  # Chroma will embed this for you
        n_results=3  # how many results to return
    )
    return results

def get_response(collection_name, query_texts):
    collection = get_collection(collection_name)
    results = collection.query(
        query_texts=query_texts,  # Chroma will embed this for you
        n_results=10  # how many results to return
    )
    #return results['metadatas'][0][0]
    return results


# Função para responder ao usuário
def chatbot_response(collection_name,user_input):
    # Respostas simples do chatbot
    if user_input.lower() == "olá":
        return "Olá! Como posso ajudar você hoje?"
    elif user_input.lower() == "adeus":
        return "Tchau! Tenha um ótimo dia!"
    else:
        resposta = get_response(collection_name, user_input)
        return resposta


collection_name = "filmes_collection"


# Interface com Streamlit
st.title("Chatbot com Streamlit e BDVector")
st.write("Bem-vindo ao nosso chatbot!")

# Input do usuário
user_input = st.text_input("Digite sua mensagem:")

# Botão para enviar mensagem
if st.button("Enviar"):
    # Gerar resposta do chatbot
    response = chatbot_response(collection_name,user_input)
    st.write("Chatbot:", response)
