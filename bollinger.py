from datetime import datetime, timezone
import pandas as pd
import csv
import asyncio

periods = 20
std = 2


async def sma_std(csvreader, periods):
    sma_calculated = csvreader[-periods - 1:]['close_price'].mean()
    stddev_calculated = csvreader[-periods - 1:]['close_price'].std()
    band_higher = sma_calculated + 2*stddev_calculated
    band_lower = sma_calculated - 2*stddev_calculated
    # print("The calculated SMA: ", sma_calculated)
    return sma_calculated, stddev_calculated, band_higher, band_lower


async def trade_condition(close_price, band_higher, band_lower):
    buy_or_sell = None
    if close_price > band_higher:
        buy_or_sell = 'sell'
        # sell()
    elif close_price < band_lower:
        buy_or_sell = 'buy'
        # buy()
    else:
        buy_or_sell = '-'
        # neither buy or sell
    return buy_or_sell


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

    # Write information to the csv file
    with open('currency_info.csv', 'a', newline='') as file:
        writing = csv.writer(file)
        with open("currency_info.csv", "r") as file:
            csvreader = pd.read_csv(file)
            if len(csvreader) >= periods + 1:
                print("Proceed calculating Bollinger Bands...")

                # Calculate SMA, std, higher, lower
                sma_calculated, stddev_calculated, band_higher, band_lower = await sma_std(
                    csvreader, periods)

                # Check if trade condition is met: Close price cross band
                buy_or_sell = await trade_condition(
                    float(close_price), band_higher, band_lower)

                # Updat CSV
                writing.writerow(
                    [open_price, close_price, high_price, low_price, sma_calculated, band_higher, band_lower, buy_or_sell])
                print(len(csvreader))
            else:
                writing.writerow(
                    [open_price, close_price, high_price, low_price, 'Nah', 'Nah', 'Nah', 'Nah'])
                print(len(csvreader))

        file.close()


# async def time_conversion(start_time_unix, close_time_unix):
#     start_time = datetime.fromtimestamp(start_time_unix)
#     close_time = datetime.fromtimestamp(close_time_unix)

#     return start_time, close_time
#  csvreader['SMA'][-1] = csvreader[-periods - 1:]['close_price'].rolling(window=20).mean()
