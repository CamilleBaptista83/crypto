from flask import Flask, render_template, redirect, request
import mysql.connector
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import os

def create_app():
    app = Flask(__name__)

    baseDeDonnees = mysql.connector.connect(host=os.environ.get('DB_HOST'),user=os.environ.get('DB_USER'),password=os.environ.get('DB_PASSWD'), database=os.environ.get('DB_NAME'))
    headers = { 'X-CMC_PRO_API_KEY' : os.environ.get('X-CMC_PRO_API_KEY')}

    @app.route("/")
    def home():
        #BDD APPEL
        curseur = baseDeDonnees.cursor()
        curseur.execute("SELECT crypto, SUM(quantite) FROM mes_cryptos GROUP BY crypto")
        mes_cryptos = curseur.fetchall()
        baseDeDonnees.close()
        print(mes_cryptos)
        #API POUR LES COMPARAISONS
        api_cryptos = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?aux=cmc_rank',headers=headers)
        api_cryptos = api_cryptos.json()['data']
        #CALCULS DU PRIX TOTAL 
        total_prix = 0
        for crypto in mes_cryptos:
            for api_crypto in api_cryptos:
                if crypto[0] == api_crypto['symbol']:
                    total_prix = total_prix +(api_crypto['quote']['USD']['price'] * crypto[1])

        return render_template('pages/home.html', mes_cryptos = mes_cryptos, total_prix = round(total_prix, 2), api_cryptos=api_cryptos)
    
    @app.route("/graphique")
    def graphique():
        curseur = baseDeDonnees.cursor()
        df_mes_cryptos = pd.io.sql.read_sql('SELECT * FROM every_day', baseDeDonnees)
        baseDeDonnees.close()

        img = io.BytesIO()
        
        plt.figure(figsize=(16,8), facecolor = 'black')
        plt.plot(df_mes_cryptos.jour, df_mes_cryptos.montant, c='white', lw=6)
        plt.axis('off')
        plt.xlabel('Dates')
        plt.ylabel('Incomes ($)')
        plt.title('Élution du CA sur la période 2018 - 2020')
        plt.xticks(df_mes_cryptos.jour[::1])

        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)

        image = base64.b64encode(img.getvalue()).decode('utf8')
        return render_template('pages/graph.html', image=image)

    @app.route("/add")
    def add():
        #API POUR LES OPTIONS
        api_crypto = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?aux=cmc_rank',headers=headers)
        api_crypto = api_crypto.json()['data']
        api_crypto
        return render_template('pages/add.html', api_crypto = api_crypto)

    @app.route("/post-add", methods=['POST'] )
    def postAdd():
        #BDD APPEL
        curseur = baseDeDonnees.cursor()
        new_crypto = (request.form['crypto'],  request.form['quantite'], request.form['prix'])
        curseur.execute("INSERT INTO mes_cryptos (crypto, quantite, prix) VALUES (%s, %s, %s)", new_crypto)
        baseDeDonnees.commit()
        baseDeDonnees.close()
        return redirect('/')

    @app.route("/modify")
    def modify():
        curseur = baseDeDonnees.cursor()
        curseur.execute("SELECT * FROM mes_cryptos")
        mes_cryptos = curseur.fetchall()
        curseur.execute("SELECT crypto, count(*) AS 'nombre_de_crypto' FROM mes_cryptos GROUP BY crypto")
        nom_cryptos = curseur.fetchall()
        baseDeDonnees.close()
        return render_template('pages/modify.html', mes_cryptos = mes_cryptos, nom_cryptos=nom_cryptos)
        
    @app.route("/modify-one/<string:crypto>")
    def modifyOne(crypto):
        crypto_selected = crypto
        return render_template('pages/modifyOne.html', crypto_selected = crypto_selected)
        
    @app.route("/vendre", methods=['POST'] )
    def vendre():
        #BDD APPEL
        curseur = baseDeDonnees.cursor()
        vendre_crypto = (request.form['crypto'],  request.form['quantite'], request.form['prix'])
        curseur.execute("INSERT INTO mes_cryptos (crypto, quantite, prix) VALUES (%s, -1 *(%s), %s)", vendre_crypto)
        baseDeDonnees.commit()
        baseDeDonnees.close()
        return redirect('/')


    @app.route("/get-data-for-js")
    def getDataForJs():
        #API
        api_cryptos = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?aux=cmc_rank',headers=headers)
        api_cryptos = api_cryptos.json()
        return api_cryptos

    @app.route("/get-database-for-js")
    def getDataBaseForJs():
        #API
        cryptoWanted = request.args.get('cryptowanted')
        curseur = baseDeDonnees.cursor()
        curseur.execute(" SELECT SUM(quantite) FROM mes_cryptos WHERE crypto = (%s)", (cryptoWanted, )) 
        cryptoSelected = curseur.fetchall()       
        baseDeDonnees.close()
        df_cryptoSelected = pd.DataFrame(cryptoSelected).T
        dictionaryObject = df_cryptoSelected.to_dict()
        return dictionaryObject

    @app.route("/daily")
    def daily():
        #BDD APPEL
        curseur = baseDeDonnees.cursor()
        curseur.execute("SELECT crypto, SUM(quantite) FROM mes_cryptos GROUP BY crypto")
        mes_cryptos = curseur.fetchall()
        print(mes_cryptos)
        #API POUR LES COMPARAISONS
        api_cryptos = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?aux=cmc_rank',headers=headers)
        api_cryptos = api_cryptos.json()['data']
        #CALCULS DU PRIX TOTAL 
        total_prix = 0
        for crypto in mes_cryptos:
            for api_crypto in api_cryptos:
                if crypto[0] == api_crypto['symbol']:
                    total_prix = total_prix +(api_crypto['quote']['USD']['price'] * crypto[1])

        curseur.execute("INSERT INTO every_day (montant, jour) VALUES (%s, NOW())", (total_prix, ))
        baseDeDonnees.commit()
        baseDeDonnees.close()

    return app

app = create_app()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
