from binance.client import Client
import json

f = open('../config.json')
config = json.load(f)

client = Client(
    api_key=config['test_net_futures']['api_key'],
    api_secret=config['test_net_futures']['secure_key'],
    testnet=True
)

client.API_URL = "https://testnet.binancefuture.com/fapi"

