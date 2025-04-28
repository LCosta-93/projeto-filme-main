import streamlit as st

# Função para responder ao usuário
def chatbot_response(user_input):
    # Respostas simples do chatbot
    if user_input.lower() == "olá":
        return "Olá! Como posso ajudar você hoje?"
    elif user_input.lower() == "adeus":
        return "Tchau! Tenha um ótimo dia!"
    else:
        return f"Você disse: {user_input}!"

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
