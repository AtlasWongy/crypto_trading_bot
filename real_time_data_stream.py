from datetime import datetime, timezone
import asyncio
import json
import websockets
import sys

# Set the base URL for the Binance API
# base_url = "wss://fstream.binance.com/ws"

# Set the symbol for the commodity
# symbol = "ETHBUSD"

# Set the ping interval in seconds
# ping_interval = 300

async def ping(websocket, ping_interval):
    while True:
            await asyncio.sleep(ping_interval)
            await websocket.ping()

async def get_current_price(config):
    # Connect to the websocket endpoint
    endpoint = f"{config['base_url']}/{config['symbol'].lower()}@kline_5m"
    while True:
        try:
            async with websockets.connect(endpoint) as websocket:
                # Send the API key and secret to authenticate the connection
                payload = {
                    
                }
                await websocket.send(json.dumps(payload))

                # Create an asyncio task to send a pong frame every 5 mins
                asyncio.create_task(ping(websocket, config['ping_interval']))

                # Continously receive data from the websocket
                async for message in websocket:
                    try:
                        data = json.loads(message)
                        current_price = data['k']['c']
                        print(f"Current price of {config['symbol']}: {current_price} ({datetime.now()} - {datetime.now(timezone.utc).timestamp()*1000 - data['E']})")
                        if data['k']['x']:
                            candlestick_data = data['k']
                            print(f"5 minute candlestick data: {candlestick_data}")
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

