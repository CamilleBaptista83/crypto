from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
        baseDeDonnees = mysql.connector.connect(host="i54jns50s3z6gbjt.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",user="o5q7ys45hd9rm28z",password="kb3khvmwsobs9ol6", database="os1rnwtjjd7h2evx")
        curseur = baseDeDonnees.cursor()
        curseur.execute("SELECT * FROM mes_cryptos")
        mes_cryptos = curseur.fetchall()

        df_mes_cryptos = pd.DataFrame(mes_cryptos)
        total_prix = df_mes_cryptos[3].sum()

        curseur.execute("INSERT INTO every_day (montant, jour) VALUES (%s, NOW())", total_prix)
        baseDeDonnees.commit()

sched.start()