# Escopo do projeto
O Projeto é constituido por 2 rotas de APIs, sendo:

GNEWS (GET)

Utilizando o script "usingAPI" com a função gnews(get), poderemos extrair todos os valores que estão armazenados dentro do dataframe

GNEWS(POST)

Utilizando o script "usingAPI" com a função gnews(post), poderemos fazer inserção de mais valores dependendo do tipo da categoria passada na propria função. Segue exemplo de como seria utilizado a função:

GNEWS("post", "business")

Categorias disponibilizadas pela api: general, world, nation, business, technology, entertainment, sports, science e health

MEANING_CLOUD()

Utilizando o script "usingAPI" com a função meaning_cloud, ele fará uma varredura das noticias que não tem um sentimento atribuido e fará a analise daquelas. Caso não exista valores de sentimento vazios, a API identificará isso e apenas irá retornar o dataframe
