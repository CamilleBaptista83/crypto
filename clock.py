from apscheduler.schedulers.blocking import BlockingScheduler
import mysql.connector
import requests

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=3)
def timed_job():
        #BDD APPEL
        baseDeDonnees = mysql.connector.connect(host="i54jns50s3z6gbjt.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",user="o5q7ys45hd9rm28z",password="kb3khvmwsobs9ol6", database="os1rnwtjjd7h2evx")
        curseur = baseDeDonnees.cursor()
        # curseur.execute("SELECT * FROM mes_cryptos")
        curseur.execute("SELECT crypto, SUM(quantite) FROM mes_cryptos GROUP BY crypto")
        mes_cryptos = curseur.fetchall()
        print(mes_cryptos)
        #API POUR LES COMPARAISONS
        headers = { 'X-CMC_PRO_API_KEY' : 'da42f614-1cf8-4c99-86ff-d8aaa4a24602'}
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

sched.start()