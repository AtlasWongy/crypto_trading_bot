import asyncio
import hashlib
import hmac
import json
import time
import requests

# API for create new order: https://binance-docs.github.io/apidocs/delivery/en/#new-order-trade
# TRADE	endpoint requires sending a valid API-Key and signature.
HTTP_TOO_MANY_REQUESTS = 429
HTTP_TIME_OUT = 408
SLEEP_TIME = 5


# TODO at main flow: When a 429 is received,
# it's your obligation as an API to back off and not spam the API (that's why sleep )
# if resp.status_code == HTTP_TOO_MANY_REQUESTS:
#     asyncio.sleep(SLEEP_TIME)
# return

async def check_server_time(config) -> int:
    endpoint = f"{config['http_base_url_test']}/fapi/v1/time"
    response = requests.get(url=endpoint)

    server_time_dict_in_bytes = response.content
    server_time_dict_in_string = server_time_dict_in_bytes.decode()

    server_time_dict = json.loads(server_time_dict_in_string)
    server_time = server_time_dict['serverTime']
    server_time_int = int(server_time)

    print(server_time_int)
    return server_time_int


async def ping_server(config) -> None:
    endpoint = f"{config['http_base_url_test']}/fapi/v1/time"
    response = requests.get(url=endpoint)

    print(response.status_code)


async def execute_order(config, symbol, price, quantity, current_server_time, side):
    endpoint = f"{config['http_base_url_test']}/fapi/v1/order"
    data = await createDataAndSignature(config['test_net_futures']['secure_key'], symbol, price, quantity,
                                        current_server_time, side)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-MBX-APIKEY": config['test_net_futures']['api_key']
    }
    # headers = {"Content-Type": "application/x-www-form-urlencoded", "X-MBX-APIKEY":config['api_key']}

    try:
        resp = requests.post(url=endpoint, headers=headers, data=data, timeout=10)
        print("The status code: ", resp.status_code)
        print("The response: ", resp.content)
        return resp.status_code
    except requests.Timeout as error:
        # if timeout then just return
        print("Order execution failed due to timeout: " + error)
        return HTTP_TIME_OUT


async def hashing(secret_key, query_string):
    return hmac.new(
        secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()


async def createDataAndSignature(secretKey, symbol, price, quantity, server_time, side):
    symbol = symbol
    side = side
    type = "LIMIT"
    timeInForce = 'GTC'
    price = price
    quantity = quantity
    timestamp = server_time
    signatureString = f"symbol={symbol}&side={side}&type={type}&quantity={quantity}&price={price}&timeInForce={timeInForce}&timestamp={timestamp}"
    signature = await hashing(secretKey, signatureString)

    data = {
        "symbol": symbol,
        "side": side,
        "type": type,
        "quantity": quantity,
        "price": price,
        "timeInForce": timeInForce,
        "timestamp": timestamp,
        "signature": signature
    }
    return data


# async def test():
#     f = open('config.json')
#     config = json.load(f)
#     current_server_time = await check_server_time(config)
#     await ping_server(config)
#     await execute_order(config, "ETHUSDT", 1599.47, 10, current_server_time)
#
#
# if __name__ == "__main__":
#     asyncio.run(test())
