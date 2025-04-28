import json
from datetime import datetime, date
from decimal import Decimal

import duckdb


def conectar_db():
    # Conecta ao banco de dados DuckDB
    return duckdb.connect('../dados/filme_duckdb.db')


# Custom serializer for non-serializable types
def custom_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Tipo {type(obj)} não é serializável")

# Function to save data into a JSON file
def salvar_em_json(dados, file_path):
    with open(file_path, 'w') as file:
        json.dump(dados, file, indent=4, default=custom_serializer)


def carregar_dados_filmes():
    # Conecta ao banco de dados DuckDB
    conexao = conectar_db()
    # Executa a consulta SQL para obter os dados
    query = 'SELECT id,Title,Year FROM filmes_imdb ORDER BY Random() LIMIT 10'

    # Executa a query e salva o resultado
    resultado = conexao.execute(query)

    # Obtém os nomes das colunas
    colunas = [desc[0] for desc in resultado.description]

    # Obtém os dados
    dados = resultado.fetchall()

    # Combina colunas e dados em uma lista de dicionários
    dados_dict = [dict(zip(colunas, linha)) for linha in dados]

    conexao.close()

    return dados_dict


# Main execution: read data and save into JSON files
if __name__ == "__main__":
    dados_filmes = carregar_dados_filmes()
    salvar_em_json(dados_filmes, "filmes.json")

    print("Dados salvos em 'filmes.json'.")
