import requests
import json
import locale

def gnews(method, category = "general"):
    method = method.upper()
    if method == 'GET':
        print("entrou")
        print(requests.get('http://127.0.0.1:5000/gnews').json())
    
    # ADICIONAR MAIS NOTICIAS REFERENTE A TODAS AS CATEGORIAS DISPONIBILIZADAS NO SITE - "general, world, nation, business, technology, entertainment, sports, science and health."
    elif method == 'POST':
        print(requests.post('http://127.0.0.1:5000/gnews', json=({"category": category})).json())

def meaning_cloud():
        print(requests.post('http://127.0.0.1:5000/meaning-cloud').json())

gnews("post", "world")