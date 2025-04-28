#importar Bibliotecas
import csv
import duckdb
import pandas as pd
import os
from datetime import datetime


print('Criando tabelas no DuckDB...')
start = datetime.now()
print('Início:', start)


# Conecta abrindo / criando um arquivo
conexao = duckdb.connect('../dados/filme_duckdb.db')

def create_table(conexao, table_name, cabecalho, dados):
    # Converte para um DataFrame e depois para uma lista de dicionários
    df = pd.DataFrame(dados.values(), columns=cabecalho)
    query = f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            AS
            SELECT * FROM df;
            '''
    conexao.execute(query)
    conexao.commit()

# Criar um dicionário para armazenar os dados únicos de writers
def create_dict_unique(data):
    dados = {}
    i = 1
    for row in data:
        linha = row[0].replace('[', '').replace(']', '').replace("'",'')
        if ',' in linha:
            # Dividindo a variável usando '||' como delimitador
            lista_row = linha.split(",")
            for item_lista in lista_row:
                dados[i] = [i,item_lista]
            i += 1
        else:
            dados[i] = [i,linha]
            i += 1
    return dados

def get_dados_filme(conexao,coluna):
    query = f'''
            SELECT
                DISTINCT {coluna}
            FROM filmes_imdb
            WHERE {coluna} IS NOT NULL
            AND {coluna} != ''
                '''
    return conexao.execute(query).fetchall()

def gerar_dados(conexao,coluna,table_name,cabecalho):
    rows = get_dados_filme(conexao,coluna)
    dados = create_dict_unique(rows)
    create_table(conexao, table_name, cabecalho, dados)


def create_table_filmes(conexao):
    # Criar a tabela filmes (se não existir)
    query = '''
            CREATE TABLE IF NOT EXISTS filmes
            AS
            SELECT  DISTINCT
                    ID,
                    UPPER(Title) as Title,
                    "Movie Link" as Link,
                    Year,
                    Duration,
                    MPA,
                    Rating,
                    Votes
            FROM filmes_imdb
            WHERE Title IS NOT NULL
            AND Title != '';
            '''
    conexao.execute(query)
    conexao.commit()

def create_table2(conexao, table_name, idtable):
    # Criar a tabela locations (se não existir)
    conexao.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name}(
                    idfilme VARCHAR(50),
                    {idtable} INTEGER
                )
    ''')
    conexao.commit()


def insert_table(conexao, table_name, table_name2, cabecalho,coluna_filme):

    # Buscar os dados de countries da tabela countries
    query = f'''
                SELECT
                    {cabecalho[0]}, {cabecalho[1]}
                FROM {table_name}
                '''
    print('------------------------------------')
    print(query)
    rows = conexao.execute(query).fetchall()
    #print(rows)
    # Criar um dicionário para armazenar os dados únicos de countries
    for row in rows:
        idtable = row[0]
        name = row[1].replace('"', "") # Remove aspas duplas do nome do countrie
        query = f'''
                SELECT
                    id
                FROM filmes_imdb
                WHERE {coluna_filme} LIKE '%{name}%'
                '''
        print('#####################################')
        print(query)
        conexao.execute(query)
        rows_filmes = conexao.fetchall()
        for row_filmes in rows_filmes:
            idfilme = row_filmes[0]
            #idtable = row_filmes[1]
            query = f'''INSERT INTO {table_name2} (idfilme,{cabecalho[0]}) \
                        VALUES
                        ('{idfilme}',{idtable});'''
            print(query)
            conexao.execute(query)

        conexao.commit()

def insert_table2(conexao, table_name, table_name2, cabecalho,coluna_filme):
    print(table_name)

    # Buscar os dados de countries da tabela countries
    query = f'''
                SELECT
                    {cabecalho[0]}, {cabecalho[1]}
                FROM {table_name}
                '''
    rows = conexao.execute(query).fetchall()
    #print(rows)
    # Criar um dicionário para armazenar os dados únicos de countries
    for row in rows:
        idtable = row[0]
        name = row[1].replace('"', "").strip() # Remove aspas duplas do nome do countrie
        query = f'''
                INSERT INTO {table_name2} (idfilme,{cabecalho[0]})
                SELECT
                    id,{idtable}
                FROM filmes_imdb
                WHERE {coluna_filme} LIKE '%{name}%'
                '''
        #print('#####################################')
        #print(query)
        conexao.execute(query)

        conexao.commit()



# Criar a tabela filmes (se não existir)
create_table_filmes(conexao)

# Criar um dicionário para armazenar os dados únicos
coluna_filme = "countries_origin"
table_name = "countries"
cabecalho = ["idcountrie","countrie"]
gerar_dados(conexao,coluna_filme,table_name,cabecalho)
table_name2 = 'filmes_countries'
idtable = 'idcountrie'
create_table2(conexao, table_name2, idtable)
insert_table2(conexao, table_name, table_name2, cabecalho,coluna_filme)


coluna_filme = "directors"
table_name = "directors"
cabecalho = ["iddirector","director"]
gerar_dados(conexao,coluna_filme,table_name,cabecalho)
table_name2 = 'filmes_directors'
idtable = 'iddirector'
create_table2(conexao, table_name2, idtable)
insert_table2(conexao, table_name, table_name2, cabecalho,coluna_filme)


coluna_filme = "genres"
table_name = "genres"
cabecalho = ["idgenre","genre"]
gerar_dados(conexao,coluna_filme,table_name,cabecalho)
table_name2 = 'filmes_genres'
idtable = 'idgenre'
create_table2(conexao, table_name2, idtable)
insert_table2(conexao, table_name, table_name2, cabecalho,coluna_filme)


coluna_filme = "languages"
table_name = "languages"
cabecalho = ["idlanguage","language"]
gerar_dados(conexao,coluna_filme,table_name,cabecalho)
table_name2 = 'filmes_languages'
idtable = 'idlanguage'
create_table2(conexao, table_name2, idtable)
insert_table2(conexao, table_name, table_name2, cabecalho,coluna_filme)

coluna_filme = "filming_locations"
table_name = "locations"
cabecalho = ["idlocation","location"]
gerar_dados(conexao,coluna_filme,table_name,cabecalho)
table_name2 = 'filmes_locations'
idtable = 'idlocation'
create_table2(conexao, table_name2, idtable)
insert_table2(conexao, table_name, table_name2, cabecalho,coluna_filme)


coluna_filme = "stars"
table_name = "stars"
cabecalho = ["idstar","star"]
gerar_dados(conexao,coluna_filme,table_name,cabecalho)
table_name2 = 'filmes_stars'
idtable = 'idstar'
create_table2(conexao, table_name2, idtable)
insert_table2(conexao, table_name, table_name2, cabecalho,coluna_filme)


coluna_filme = "writers"
table_name = "writers"
cabecalho = ["idwriter","writer"]
gerar_dados(conexao,coluna_filme,table_name,cabecalho)
table_name2 = 'filmes_writers'
idtable = 'idwriter'
create_table2(conexao, table_name2, idtable)
insert_table2(conexao, table_name, table_name2, cabecalho,coluna_filme)



# Commitar as alterações
conexao.commit()

# Fechar a conexão
conexao.close()

stop = datetime.now()
print('Termino:', stop)
