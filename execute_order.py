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

async def byte_unpack_loader(response_in_bytes):
    response_dict_in_string = response_in_bytes.decode()
    response_dict = json.loads(response_dict_in_string)
    return response_dict


async def check_order_status(config, symbol, order_id):
    endpoint = f"{config['http_base_url_test']}/fapi/v1/openOrder"
    data = await createDataAndSignature(
        config=config,
        secretKey=config['test_net_futures']['secure_key'],
        symbol=symbol,
        order_id=order_id,
        execution_type='CHECK_ORDER'
    )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-MBX-APIKEY": config['test_net_futures']['api_key']
    }

    try:
        response = requests.get(url=endpoint, headers=headers, params=data)
        response_unloaded = await byte_unpack_loader(response.content)
        print("The response: ", response_unloaded)
        order_status = response_unloaded['status']

        print("The order status is: ", order_status)

        return order_status
    except (requests.Timeout, KeyError) as error:
        # if timeout then just return
        # print("Order execution failed due to timeout: " + error)
        print("Error due to: ", error)
        return HTTP_TIME_OUT


async def check_server_time(config) -> int:
    endpoint = f"{config['http_base_url_test']}/fapi/v1/time"
    response = requests.get(url=endpoint)
    response_unloaded = await byte_unpack_loader(response.content)

    server_time_string = response_unloaded['serverTime']
    server_time = int(server_time_string)

    return server_time


async def ping_server(config) -> None:
    endpoint = f"{config['http_base_url_test']}/fapi/v1/time"
    response = requests.get(url=endpoint)

    print(response.status_code)


async def execute_order(config, symbol, price, quantity, current_server_time, side, execution_type):
    endpoint = f"{config['http_base_url_test']}/fapi/v1/order"
    data = await createDataAndSignature(
        config=config,
        secretKey=config['test_net_futures']['secure_key'],
        symbol=symbol,
        price=price,
        quantity=quantity,
        server_time=current_server_time,
        side=side,
        execution_type=execution_type
    )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-MBX-APIKEY": config['test_net_futures']['api_key']
    }

    try:
        resp = requests.post(url=endpoint, headers=headers, data=data, timeout=10)
        print("The status code: ", resp.status_code)

        response_unloaded = await byte_unpack_loader(resp.content)
        print(response_unloaded)
        order_id = response_unloaded['orderId']

        return resp.status_code, order_id
    except requests.Timeout as error:
        # if timeout then just return
        print("Order execution failed due to timeout: " + error)
        return HTTP_TIME_OUT


async def hashing(secret_key, query_string):
    return hmac.new(
        secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()


async def createDataAndSignature(
        config, secretKey, symbol, price=0, quantity=0, server_time=0, side='', execution_type='', order_id='0'):

    if execution_type == "LIMIT":

        print("The current server time: ", server_time)

        symbol = symbol
        side = side
        type = execution_type
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
            "signature": signature,
        }

        return data
    elif execution_type == "CHECK_ORDER":
        server_time = await check_server_time(config=config)
        signature_string = f"symbol={symbol}&orderId={order_id}&timestamp={server_time}&recvWindow={5000}"
        signature = await hashing(secretKey, signature_string)

        data = {
            "symbol": symbol,
            "orderId": order_id,
            "timestamp": server_time,
            "recvWindow": 5000,
            "signature": signature
        }

        return data

    else:
        return


async def test():
    f = open('config.json')
    config = json.load(f)
    current_server_time = await check_server_time(config)
    await ping_server(config)

    # Execute
    status_code, order_id = await execute_order(config, "ETHUSDT", 1400, 10, current_server_time, "BUY", "LIMIT")

    # Check if order is finished
    while await check_order_status(config=config, symbol="ETHUSDT", order_id=order_id) != "FILLED":
        time.sleep(5)
        print("order is not fulfilled....")
        continue
    # Web Socket
    # Yi Jie

    # Stop
    # Hui Wen

    # Take Profit
    # Hui Wen


if __name__ == "__main__":
    asyncio.run(test())
