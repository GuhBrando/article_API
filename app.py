from flask import Flask
from flask import request
import pandas as pd
import urllib.request
import requests
import ssl
import json
from datetime import datetime
from flask import Flask, request, jsonify, abort
import werkzeug.exceptions

API_GNEWS = "1d7c0817c539f449c5bbae10724fff81"
url_gnews = 'https://gnews.io/api/v4/search?q=example&lang=ept&country=us&max=10&apikey=' + API_GNEWS

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
apikey = "1d7c0817c539f449c5bbae10724fff81"
category = "general"
url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max=10&apikey={apikey}"

try:
    article_dataframe = pd.read_csv(r"C:\Users\TheDa\Documents\GitHub\ingestão-eng-dados\projeto\banco_dados.csv")
except:
    pass

with urllib.request.urlopen(url, context=ctx) as response:
    data = json.loads(response.read().decode("utf-8"))
    articles = data["articles"]
    for i in range(len(articles)):
        post_url = articles[i]['url']
        title = articles[i]['title']
        if bool(post_url in article_dataframe["post_url"].values) != True:
            description = articles[i]['description']
            content = articles[i]['content']
            published_at = articles[i]['publishedAt']
            commit_query = {"title": title, "description": description, "content": content, "published_at": published_at, "post_url": post_url}
            article_dataframe = article_dataframe.append(commit_query, ignore_index=True)
        else:
            print(f"{title} | Ja existe no dataframe")
            
article_dataframe.to_csv(r"C:\Users\TheDa\Documents\GitHub\ingestão-eng-dados\projeto\banco_dados.csv", index = False)

app = Flask(__name__)

@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify('Categoria invalida, valor revalidar!'), 400

@app.route("/gnews", methods = ["GET", "POST"])
def gnews():
    apikey = "1d7c0817c539f449c5bbae10724fff81"
    article_dataframe = pd.read_csv(r"C:\Users\TheDa\Documents\GitHub\ingestão-eng-dados\projeto\banco_dados.csv")
    
    # MOSTRAR TODOS OS VALORES DO DATAFRAME
    if request.method == 'GET':
        return article_dataframe.to_json()
    
    # ADICIONAR MAIS NOTICIAS REFERENTE A TODAS AS CATEGORIAS DISPONIBILIZADAS NO SITE - "general, world, nation, business, technology, entertainment, sports, science and health."
    elif request.method == 'POST':
        valid_categories = ["general", "world", "nation", "business", "technology", "entertainment", "sports", "science", "health"]
        category = request.json['category']
        if category not in valid_categories:
            abort(400)
            
        url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max=10&apikey={apikey}"
        with urllib.request.urlopen(url, context=ctx) as response:
            data = json.loads(response.read().decode("utf-8"))
            articles = data["articles"]
            for i in range(len(articles)):
                post_url = articles[i]['url']
                title = articles[i]['title']
                if bool(post_url in article_dataframe["post_url"].values) != True:
                    description = articles[i]['description']
                    content = articles[i]['content']
                    published_at = articles[i]['publishedAt']
                    commit_query = {"title": title, "description": description, "content": content, "published_at": published_at, "post_url": post_url}
                    article_dataframe = article_dataframe.append(commit_query, ignore_index=True)
                    article_dataframe.to_csv(r"C:\Users\TheDa\Documents\GitHub\ingestão-eng-dados\projeto\banco_dados.csv", index = False)
                else:
                    print(f"{title} | Ja existe no dataframe")
        return article_dataframe.to_json()

@app.route("/meaning-cloud", methods = ["POST"])
def meaning_cloud():
    article_dataframe = pd.read_csv(r"C:\Users\TheDa\Documents\GitHub\ingestão-eng-dados\projeto\banco_dados.csv")
    URL_MEANING_CLOUD = "https://api.meaningcloud.com/sentiment-2.1"
    if request.method == 'POST':
        article_dataframe_descriptions = article_dataframe[article_dataframe["sentiment"].isna()]
        descriptions = article_dataframe_descriptions["description"].values
        for single_description in descriptions:
            payload={
                'key': '31a77a35fa595c94df9b46d8c0a26dd8',
                'txt': str(single_description), 
                'lang': 'en',
            }

            sentiment = requests.post(URL_MEANING_CLOUD, data=payload)
            print(sentiment.json()["score_tag"])
            article_dataframe.loc[article_dataframe["description"] == single_description, "sentiment"] = sentiment.json()["score_tag"]
        article_dataframe.to_csv(r"C:\Users\TheDa\Documents\GitHub\ingestão-eng-dados\projeto\banco_dados.csv", index = False)
        return article_dataframe.to_json()
        
if __name__ == "__main__":
    app.run
