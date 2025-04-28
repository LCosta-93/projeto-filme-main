from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import streamlit as st
import re

# TEMPERATURA AJUSTÁVEL
temp = st.slider("🌡️ Temperatura do Modelo", 0.0, 1.0, 0.2)
model = ChatGroq(model="llama-3.1-8b-instant", temperature=temp)

# TÍTULO DO STREAMLIT
st.title("Nyra")    
st.write("🦊 Bem-vindo!")

# INICIALIZAR O HISTÓRICO DE MENSAGENS
if "history" not in st.session_state:
    st.session_state.history = []

# FUNÇÃO PARA VERIFICAR REPETIÇÃO EXCESSIVA DE UMA MESMA LETRA
def repeticao_excessiva(texto):
    texto_limpo = re.sub(r"[^a-zA-Z]", "", texto.lower())
    return len(set(texto_limpo)) == 1 and len(texto_limpo) >= 5

# FUNÇÃO PARA DETECTAR OFENSAS
def contem_ofensa(texto):
    palavras_ofensivas = ["idiota", "burra", "estúpida", "inútil", "otária", "feia", "lenta"]
    texto_lower = texto.lower()
    return any(palavra in texto_lower for palavra in palavras_ofensivas)

# FUNÇÃO PARA GERAR RESPOSTA DO CHATBOT (NYRA)
def chatbot_response(user_input):
    if user_input.lower() == "olá":
        return "Olá! Vir falar comigo foi a melhor decisão que você tomou hoje!"
    elif user_input.lower() == "adeus":
        return "Tchau! Boa sorte em lidar com o mundo sem minha ajuda!"
    elif repeticao_excessiva(user_input):
        return "AAAAAAAAAAAAAH!"
    elif contem_ofensa(user_input):
        return "Oh, tá nervosinho é?"
    else:
        prompt = (
            "Você é Nyra, uma assistente virtual,"
            "direta, objetiva.\n\n"
            f"Pergunta: {user_input}\nResposta:"
        )
        resposta = model.invoke([HumanMessage(content=prompt)])
        return resposta.content

# MOSTRAR O HISTÓRICO DE MENSAGENS
for role, msg in st.session_state.history:
    if role == "Você":
        st.write(f"**{role}:** {msg}")
    elif role == "Nyra":
        st.write(f"**{role}:** {msg}")

# SEPARADOR VISUAL (OPCIONAL)
st.divider()

# FORMULÁRIO DE INPUT
with st.form(key="formulario_mensagem", clear_on_submit=True):
    user_input = st.text_input("Mensagem:")
    submit_button = st.form_submit_button("Enviar")

# TRATAR ENVIO
if submit_button and user_input:
    response = chatbot_response(user_input)
    st.session_state.history.append(("Você", user_input))
    st.session_state.history.append(("Nyra", response))