import chromadb
chroma_client = chromadb.Client()

# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
collection = chroma_client.get_or_create_collection(name="filmes")

# switch `add` to `upsert` to avoid adding the same documents every time
collection.upsert(
    documents=[
        "O filme Proud American foi lançado em 2008",
        "O filme Good Boy foi lançado em 2022",
        "O filme Sex with Strangers foi lançado em 2002",
        "O filme C.B. Hustlers foi lançado em 1976",
        "O filme Generation Iron foi lançado em 2013",
        "O filme Monkey Warfare foi lançado em 2006",
        "O filme I Saw What You Did foi lançado em 1965",
        "O filme Beautiful Creatures foi lançado em 2013",
        "O filme Run and Kill foi lançado em 1993",
        "O filme Thunderbolt and Lightfoot foi lançado em 1974"
    ],
    ids=["tt1008023","tt19705884","tt0304692","tt0310837","tt2205904","tt0832906","tt0059297","tt1559547","tt0108600","tt0072288",]
)

results = collection.query(
    query_texts=["Qual filme lançado antes do ano 2002"], # Chroma will embed this for you
    n_results=1 # how many results to return
)

print(results)
