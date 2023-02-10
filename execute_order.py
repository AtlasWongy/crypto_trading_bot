import asyncio
import hashlib
import hmac
import json
import time
import requests

#API for create new order: https://binance-docs.github.io/apidocs/delivery/en/#new-order-trade
#TRADE	endpoint requires sending a valid API-Key and signature.
#When a 429 is received, it's your obligation as an API to back off and not spam the API. =====> Need to sleep before calculate and retry again?
HTTP_TOO_MANY_REQUESTS = 429
SLEEP_TIME = 5

def hashing(secretKey, query_string):
    return hmac.new(
        secretKey.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

def createDataAndSignature(secretKey, symbol, price, quantity):
    symbol = symbol
    side = "BUY"
    type = "LIMIT"
    timeInForce='GTC'
    price = price
    quantity = quantity
    timestamp = int(time.time() * 1000)
    signatureString = f"symbol={symbol}&side={side}&type={type}&quantity={quantity}&price={price}&timeInForce={timeInForce}&timestamp={timestamp}"
    signature = hashing(secretKey, signatureString)
    
    data = {
        "symbol":symbol,
        "side":side,
        "type":type,
        "quantity":quantity,
        "price":price,
        "timeInForce":timeInForce,
        "timestamp":timestamp,
        "signature":signature
    }
    return data

async def execute_order(config, symbol, price, quantity):
    endpoint = f"{config['http_base_url_live']}/dapi/v1/order"
    data = createDataAndSignature(config['secure_key'], symbol, price, quantity)
    headers = {"Content-Type": "application/x-www-form-urlencoded", "X-MBX-APIKEY":config['api_key']}

    try:
        resp = requests.post(url = endpoint, headers=headers, data = data, timeout=10)
        if resp.status_code == HTTP_TOO_MANY_REQUESTS:
            asyncio.sleep(SLEEP_TIME)
            return
        print(resp.content)
    except requests.Timeout as error:
        #if timeout then just return
        print("Order execution failed due to timeout: " + error)
        return

async def test():
    f = open('config.json')
    config = json.load(f)
    await execute_order(config, "DOGE", 1, 100)

if __name__ == "__main__":
    asyncio.run(test())