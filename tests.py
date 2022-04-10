import pytest
import requests
from app import create_app
import mysql.connector


@pytest.fixture
def app():
    appli = create_app()
    yield appli


@pytest.fixture()
def client(app):
    return app.test_client()


def test_ws_bdd_connexion_ok():
    baseDeDonnees = mysql.connector.connect(host="i54jns50s3z6gbjt.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",user="o5q7ys45hd9rm28z",password="kb3khvmwsobs9ol6", database="os1rnwtjjd7h2evx")
    curseur = baseDeDonnees.cursor()
    assert curseur
    baseDeDonnees.close()


def test_ws_api_ok():
    headers = { 'X-CMC_PRO_API_KEY' : 'da42f614-1cf8-4c99-86ff-d8aaa4a24602'}
    api_cryptos = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?aux=cmc_rank',headers=headers)
    assert "status" in api_cryptos.json()


def test_home_response(client):
    response = client.get('/')
    assert response.status_code == 200


# def test_groupe_politique_response(client):
#     response = client.get('/groupe-politique')
#     assert response.status_code == 200