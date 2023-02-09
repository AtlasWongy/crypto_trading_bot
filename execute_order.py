import json

#API for create new order: https://binance-docs.github.io/apidocs/delivery/en/#new-order-trade
#When a 429 is received, it's your obligation as an API to back off and not spam the API. =====> Need to sleep before calculate and retry again?

def execute_order(config):
    # Connect to the websocket endpoint
    endpoint = f"{config['http_base_url_test']}/dapi/v1/order"
    print(endpoint)


if __name__ == "__main__":
    f = open('config.json')
    config = json.load(f)
    print(execute_order(config))