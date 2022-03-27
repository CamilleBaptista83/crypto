from flask import Flask, render_template, redirect, request
import mysql.connector

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        baseDeDonnees = mysql.connector.connect(host="localhost",user="root",password="", database="crypto")
        curseur = baseDeDonnees.cursor()
        curseur.execute("SELECT * FROM mes_cryptos")
        mes_cryptos = curseur.fetchall()
        baseDeDonnees.close()
        return render_template('pages/home.html', mes_cryptos = mes_cryptos)

    @app.route("/add")
    def add():
        return render_template('pages/add.html')

    @app.route("/post-add", methods=['POST'] )
    def postAdd():
        baseDeDonnees = mysql.connector.connect(host="localhost",user="root",password="", database="crypto")
        curseur = baseDeDonnees.cursor()
        new_crypto = (request.form['crypto'],  request.form['quantite'], request.form['prix'])
        curseur.execute("INSERT INTO mes_cryptos (crypto, quantite, prix) VALUES (%s, %s, %s)", new_crypto)
        baseDeDonnees.commit()
        baseDeDonnees.close()
        return redirect('/')

    @app.route("/modify")
    def modify():
        baseDeDonnees = mysql.connector.connect(host="localhost",user="root",password="", database="crypto")
        curseur = baseDeDonnees.cursor()
        curseur.execute("SELECT * FROM mes_cryptos")
        mes_cryptos = curseur.fetchall()
        baseDeDonnees.close()
        return render_template('pages/modify.html', mes_cryptos = mes_cryptos)
        
    @app.route("/modify/<id>")
    def modifyOne(id):
        baseDeDonnees = mysql.connector.connect(host="localhost",user="root",password="", database="crypto")
        curseur = baseDeDonnees.cursor()
        curseur.execute("SELECT * FROM mes_cryptos WHERE id = (%s)", (id, ))
        crypto_selected = curseur.fetchone()
        baseDeDonnees.close()
        return render_template('pages/modifyOne.html', crypto_selected = crypto_selected)

    @app.route("/post-modify/<id>", methods=['POST'] )
    def postModify(id):
        baseDeDonnees = mysql.connector.connect(host="localhost",user="root",password="", database="crypto")
        curseur = baseDeDonnees.cursor()
        update_crypto = (request.form['crypto'],  request.form['quantite'], request.form['prix'], id)
        curseur.execute("UPDATE mes_cryptos SET crypto=%s, quantite=%s, prix=%s WHERE id=%s", update_crypto)
        baseDeDonnees.commit()
        baseDeDonnees.close()
        return redirect('/')
        
    @app.route("/delete/<int:id>")
    def delete(id):
        baseDeDonnees = mysql.connector.connect(host="localhost",user="root",password="", database="crypto")
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
