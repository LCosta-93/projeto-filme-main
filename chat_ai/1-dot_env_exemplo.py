from dotenv import load_dotenv
load_dotenv()
import os

api_key_anthropic = os.getenv("ANTHROPIC_API_KEY")
api_key_google = os.getenv("GOOGLE_API_KEY")


api_key_qdrant = os.getenv("QDRANT_API_KEY")

file_duckdb = os.getenv("DUCK_FILE_PATH")

mysq_host = os.getenv("DB_MYSQL_HOST")
mysq_schema = os.getenv("DB_MYSQL_SCHEMA")
mysq_user = os.getenv("DB_MYSQL_USER")
mysq_password = os.getenv("DB_MYSQL_PASSWORD")
mysq_port = os.getenv("DB_MYSQL_PORT")

print("============== IMPRIMINDO API KEY =================================")
print(f"API_KEY ANTHROPIC: {api_key_anthropic}")
print(f"API_KEY GOOGLE: {api_key_google}")
print(f"API_KEY QDRANT: {api_key_qdrant}")

print("============== IMPRIMINDO DADOS DO DUCKDB ============================")
print(f"DUCKDB FILE: {file_duckdb}")
print("============== IMPRIMINDO DADOS DO BANCO ============================")
print(f"MYSQL HOST: {mysq_host}")
print(f"MYSQL SCHEMA: {mysq_schema}")
print(f"MYSQL USER: {mysq_user}")
print(f"MYSQL PASSWORD: {mysq_password}")
print(f"MYSQL PORT: {mysq_port}")




