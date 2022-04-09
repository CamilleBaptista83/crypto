from flask import Flask, render_template, redirect, request
import mysql.connector
import requests

import pandas as pd

# baseDeDonnees = mysql.connector.connect(host="localhost",user="root",password="admin", database="crypto")



def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        #BDD APPEL
        baseDeDonnees = mysql.connector.connect(host="i54jns50s3z6gbjt.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",user="o5q7ys45hd9rm28z",password="kb3khvmwsobs9ol6", database="os1rnwtjjd7h2evx")
        curseur = baseDeDonnees.cursor()
        curseur.execute("SELECT * FROM mes_cryptos")
        mes_cryptos = curseur.fetchall()
        baseDeDonnees.close()
        #API POUR LES COMPARAISONS
        headers = { 'X-CMC_PRO_API_KEY' : 'da42f614-1cf8-4c99-86ff-d8aaa4a24602'}
        api_cryptos = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?aux=cmc_rank',headers=headers)
        api_cryptos = api_cryptos.json()['data']
        #CALCULS DU PRIX TOTAL 
        total_prix = 0
        for crypto in mes_cryptos:
            for api_crypto in api_cryptos:
                if crypto[1] == api_crypto['symbol']:
                    total_prix = total_prix +(api_crypto['quote']['USD']['price'] * crypto[2])

        return render_template('pages/home.html', mes_cryptos = mes_cryptos, total_prix = round(total_prix, 2), api_cryptos=api_cryptos)

    @app.route("/add")
    def add():
        #API POUR LES OPTIONS
        headers = { 'X-CMC_PRO_API_KEY' : 'da42f614-1cf8-4c99-86ff-d8aaa4a24602'}
        api_crypto = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?aux=cmc_rank',headers=headers)
        api_crypto = api_crypto.json()['data']
        api_crypto
        return render_template('pages/add.html', api_crypto = api_crypto)

    @app.route("/post-add", methods=['POST'] )
    def postAdd():
        #BDD APPEL
        baseDeDonnees = mysql.connector.connect(host="i54jns50s3z6gbjt.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",user="o5q7ys45hd9rm28z",password="kb3khvmwsobs9ol6", database="os1rnwtjjd7h2evx")
        curseur = baseDeDonnees.cursor()
        new_crypto = (request.form['crypto'],  request.form['quantite'], request.form['prix'])
        curseur.execute("INSERT INTO mes_cryptos (crypto, quantite, prix) VALUES (%s, %s, %s)", new_crypto)
        baseDeDonnees.commit()
        baseDeDonnees.close()
        return redirect('/')

    @app.route("/get-data-for-js")
    def getDataForJs():
        #API
        headers = { 'X-CMC_PRO_API_KEY' : 'da42f614-1cf8-4c99-86ff-d8aaa4a24602'}
        api_cryptos = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?aux=cmc_rank',headers=headers)
        api_cryptos = api_cryptos.json()
        return api_cryptos

    @app.route("/modify")
    def modify():
        baseDeDonnees = mysql.connector.connect(host="i54jns50s3z6gbjt.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",user="o5q7ys45hd9rm28z",password="kb3khvmwsobs9ol6", database="os1rnwtjjd7h2evx")
        curseur = baseDeDonnees.cursor()
        curseur.execute("SELECT * FROM mes_cryptos")
        mes_cryptos = curseur.fetchall()
        baseDeDonnees.close()
        return render_template('pages/modify.html', mes_cryptos = mes_cryptos)
        
    @app.route("/modify/<id>")
    def modifyOne(id):
        baseDeDonnees = mysql.connector.connect(host="i54jns50s3z6gbjt.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",user="o5q7ys45hd9rm28z",password="kb3khvmwsobs9ol6", database="os1rnwtjjd7h2evx")
        curseur = baseDeDonnees.cursor()
        curseur.execute("SELECT * FROM mes_cryptos WHERE id = (%s)", (id, ))
        crypto_selected = curseur.fetchone()
        baseDeDonnees.close()
        return render_template('pages/modifyOne.html', crypto_selected = crypto_selected)

    @app.route("/post-modify/<id>", methods=['POST'] )
    def postModify(id):
        baseDeDonnees = mysql.connector.connect(host="i54jns50s3z6gbjt.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",user="o5q7ys45hd9rm28z",password="kb3khvmwsobs9ol6", database="os1rnwtjjd7h2evx")
        curseur = baseDeDonnees.cursor()
        update_crypto = (request.form['crypto'],  request.form['quantite'], request.form['prix'], id)
        curseur.execute("UPDATE mes_cryptos SET crypto=%s, quantite=%s, prix=%s WHERE id=%s", update_crypto)
        baseDeDonnees.commit()
        baseDeDonnees.close()
        return redirect('/')
        
    @app.route("/delete/<int:id>")
    def delete(id):
        baseDeDonnees = mysql.connector.connect(host="i54jns50s3z6gbjt.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",user="o5q7ys45hd9rm28z",password="kb3khvmwsobs9ol6", database="os1rnwtjjd7h2evx")
        curseur = baseDeDonnees.cursor()
        curseur.execute(" DELETE FROM mes_cryptos WHERE id = (%s)", (id, ))
        baseDeDonnees.commit()
        baseDeDonnees.close()
        return redirect('/')

    return app

app = create_app()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
