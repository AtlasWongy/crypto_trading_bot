from datetime import datetime, timezone
import pandas as pd
import csv
import asyncio

periods = 20
std = 2


async def calculate_bollinger_band(start_time, close_time, open_price, close_price, high_price, low_price):
    print("----------------")
    print("The open price: ", open_price)
    print("The close price: ", close_price)
    print("The high price: ", high_price)
    print("The low price: ", low_price)
    print("The start time: ", start_time)
    print("The close time: ", close_time)

    # Time conversion
    # Convert unix timestamp to current normal time stamp

    # Empty csv for new data

    # Write information to the csv file
    with open('currency_info.csv', 'a', newline='') as file:
        writing = csv.writer(file)
        with open("currency_info.csv", "r") as file:
            csvreader = pd.read_csv(file)
            if len(csvreader) >= periods + 1:
                print(len(csvreader))

                print("Proceed calculating Bollinger Bands...")
                sma_calculated = csvreader[-periods -
                                           1:]['close_price'].mean()
                print("The calculated SMA: ", sma_calculated)
                writing.writerow(
                    [open_price, close_price, high_price, low_price, sma_calculated])

            else:
                print(len(csvreader))
                writing.writerow(
                    [open_price, close_price, high_price, low_price, None])
        file.close()


# async def time_conversion(start_time_unix, close_time_unix):
#     start_time = datetime.fromtimestamp(start_time_unix)
#     close_time = datetime.fromtimestamp(close_time_unix)

#     return start_time, close_time
#  csvreader['SMA'][-1] = csvreader[-periods - 1:]['close_price'].rolling(window=20).mean()
