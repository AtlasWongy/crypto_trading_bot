from datetime import datetime, timezone
from bollinger import calculate_bollinger_band
import asyncio
import json
import websockets
import sys
import csv


async def ping(websocket, ping_interval):
    while True:
        await asyncio.sleep(ping_interval)
        await websocket.ping()


async def get_current_price(config):
    # Connect to the websocket endpoint
    endpoint = f"{config['base_url']}/{config['symbol'].lower()}@kline_5m"
    # clean csv for each run
    with open('currency_info.csv', 'w', newline='') as file:
        writing = csv.writer(file)
        writing.writerow(['open_price', 'close_price',
                          'high_price', 'low_price', 'SMA'])
    while True:
        try:
            async with websockets.connect(endpoint) as websocket:
                # Send the API key and secret to authenticate the connection
                payload = {
                    "apiKey": config['api_key'],
                    "secret": config['secure_key']
                }
                await websocket.send(json.dumps(payload))

                # Create an asyncio task to send a pong frame every 5 mins
                asyncio.create_task(ping(websocket, config['ping_interval']))

                # Continously receive data from the websocket
                async for message in websocket:
                    try:
                        data = json.loads(message)
                        await calculate_bollinger_band(
                            data['k']['t'],
                            data['k']['T'],
                            data['k']['o'],
                            data['k']['c'],
                            data['k']['h'],
                            data['k']['l']
                        )
                    except KeyError:
                        print("Faulty data received from API")
                        continue

                # Connection was closed by the server
                print("Websocket connection lost, attempting to reconnect.....")
        except websockets.exceptions.ConnectionClosed:
            continue


async def main():
    f = open('config.json')
    config = json.load(f)
    await get_current_price(config)


asyncio.run(main())
