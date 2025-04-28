from flask import Flask, render_template, request

import duckdb
import pandas as pd


def returnar_df(table_name):
    try:
        # Conecta abrindo / criando um arquivo
        conexao = duckdb.connect('../dados/filme_duckdb.db')
        #query = f'SELECT * FROM {table_name}'
        query = f'{table_name}'
        df = conexao.execute(query).fetchdf()
        conexao.close()
        return df
    except duckdb.ParserException as e:
        # Lidar com o erro de sintaxe
        print("Erro de sintaxe na consulta SQL:", e)


app = Flask(__name__)


# Rota para o formulário
@app.route("/", methods=["GET", "POST"])
def chatbot_form():
    if request.method == "POST":
        # Obter a mensagem do usuário do formulário
        user_message = request.form.get("message")

        # Resposta básica do chatbot
        if user_message.lower() == "olá":
            bot_response = "Olá! Como posso ajudar você hoje?"
        elif user_message.lower() == "adeus":
            bot_response = "Tchau! Tenha um ótimo dia!"
        else:
            df = returnar_df(user_message)

            if isinstance(df, pd.DataFrame):
                # Verifica se o DataFrame não está vazio
                if df.empty:
                    bot_response = f"Você disse: {user_message} e não encontrei resultados!"
                else:
                    bot_response = "Você disse:"
                    return render_template("chat2.html", user_message=user_message, bot_response=bot_response,table=df.to_html())
            else:
                bot_response = f"Você disse: {user_message}!"

        return render_template("chat.html", user_message=user_message, bot_response=bot_response)

    return render_template("chat.html")





if __name__ == "__main__":
    app.run(debug=True)