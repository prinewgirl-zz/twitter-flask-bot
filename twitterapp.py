from flask import render_template, Flask, request
from lib import TwitterModule
from lib import ManipulaExcecoes
import configparser
from tweepy import error
import sys
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(),"parametros.ini"))
consumer_key = config.get("Geral","CONSUMER_KEY")
consumer_secret = config.get("Geral","CONSUMER_SECRET")
acess_token = config.get("Geral","ACESS_TOKEN")
acess_token_secret = config.get("Geral","ACESS_TOKEN_SECRET")
user = config.get("Geral","USERNAME")


def cria_hashtag(texto):
    '''essa função recebe um texto, não retorna nada apenas envia o tweet'''
    #verifica se o texto contém no máximo 280 caracteres
    if len(texto) > 280:
        raise ManipulaExcecoes.LengthError("No. de caracteres excedido")
    else:
        if '#' in texto:
            twitter.send(texto)
        else:
            raise ManipulaExcecoes.HashtagNotFound("não contém hashtag")

def rm_hashtag(hashtag):
    '''essa função recebe uma hashtag e deleta todos os tweets feitos
    pelo usuário a usando'''
    if '#' in hashtag:
        twitter.erase_all(hashtag)
    else:
        raise ManipulaExcecoes.HashtagNotFound ("não contém hashtag")

def filtra(hashtag):
    '''essa função recebe uma hashtag e filtra todos os tweets que estão 
    sendo feitos a partir dela'''
    twitter.stream(hashtag)

try:    

    twitter = TwitterModule.ManageTwitter(consumer_key,consumer_secret,\
                                          acess_token, acess_token_secret)
    twitter.verify()



    app = Flask(__name__)
    @app.route('/', methods=['GET','POST'])
    #@app.route('/index', methods=["POST"])
    def index():
        tweet = None
        if "submit_tweet" in request.form:
            tweet = request.form
            cria_hashtag(tweet['status'])
        return render_template('index.html', title='TwitterApp')
    
except ManipulaExcecoes.LengthError as tamexce:
    print(tamexce)
    sys.exit()
except ManipulaExcecoes.HashtagNotFound as hashnot:
    print(hashnot)
    sys.exit()
except error.TweepError as error:
    print("Problema com a API do twitter")
    print(error)
    sys.exit()

        
if __name__ == "__main__":
    app.run()
    
