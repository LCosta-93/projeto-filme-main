from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

from langchain_core.messages import HumanMessage

import streamlit as st


model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
)


# Função para responder ao usuário
def chatbot_response(user_input):
    # Respostas simples do chatbot
    if user_input.lower() == "olá":
        return "Olá! Como posso ajudar você hoje?"
    elif user_input.lower() == "adeus":
        return "Tchau! Tenha um ótimo dia!"
    else:
        resposta = model.invoke([HumanMessage(content=user_input)])
        return resposta

# Interface com Streamlit
st.title("Chatbot com Streamlit")
st.write("Bem-vindo ao nosso chatbot!")

# Input do usuário
user_input = st.text_input("Digite sua mensagem:")

# Botão para enviar mensagem
if st.button("Enviar"):
    # Gerar resposta do chatbot
    response = chatbot_response(user_input)
    st.write("Chatbot:", response)
