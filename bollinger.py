from datetime import datetime, timezone
import pandas as pd
import csv
import asyncio

# I use some smaller number to test because 20*5min is too larger to test.
interval = 1  # 1min
periods = 20
# update every 1 second, x min candle stick = x*60 row of records
# hence, every 300 records >> will be one 5 min candle stick
std = 2


async def sma_std(kline_interval, periods, kline_ind):
    print(kline_interval['close_price'][kline_ind])
    cal_kline_ind = kline_ind[-periods:]
    print(cal_kline_ind)
    sma_calculated = kline_interval['close_price'][cal_kline_ind].mean()
    stddev_calculated = kline_interval['close_price'][cal_kline_ind].std()
    print(sma_calculated, stddev_calculated)
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


async def calculate_bollinger_band(start_time, close_time, open_price, close_price, high_price, low_price, is_interval_end, kline_interval):
    print("----------------")
    print("The open price: ", open_price)
    print("The close price: ", close_price)
    print("The high price: ", high_price)
    print("The low price: ", low_price)
    # print("The start time: ", start_time) #this start and close time is for the 5 min candlestick
    # print("The close time: ", close_time)

    # Time conversion
    # Convert unix timestamp to current normal time stamp

    # Write information to the csv file
    with open('currency_info.csv', 'a', newline='') as file:
        writing = csv.writer(file)
        writing.writerow(
            [start_time, close_time, open_price, close_price, high_price, low_price, is_interval_end])
        print([start_time, close_time, open_price, close_price,
              high_price, low_price, is_interval_end])
        file.close()

    with open("currency_info.csv", "r") as file_read, open('bollinger_band.csv', "r") as file_read_r:
        csvreader = pd.read_csv(file_read)
        csvreader_r = pd.read_csv(file_read_r)
        print("In interval " +
              kline_interval+"... End? "+str(is_interval_end)+"...")

        # print(len(csvreader))
        # print(csvreader)
        # print([start_time, close_time, open_price, close_price,
        #        high_price, low_price, is_interval_end])
        kline_ind = csvreader.index[csvreader['is_interval_end']
                                    == True].tolist()
        print(kline_ind)
        if (len(kline_ind) >= periods and is_interval_end == True):
            # if (len(csvreader) >= periods + 1):
            print("Proceed calculating Bollinger Bands...")
            # print(kline_ind)
            # Calculate SMA, std, higher, lower
            sma_calculated, stddev_calculated, band_higher, band_lower = await sma_std(
                csvreader, periods, kline_ind)

            # Check if trade condition is met: Close price cross band
            buy_or_sell = await trade_condition(
                float(close_price), band_higher, band_lower)
            print(start_time, close_time, open_price, close_price, high_price, low_price,
                  is_interval_end, sma_calculated, stddev_calculated, band_higher, band_lower, buy_or_sell)
            # Updat CSV
            with open('bollinger_band.csv', 'a', newline='') as file_r:
                writing_r = csv.writer(file_r)  # results file
                writing_r.writerow(
                    [start_time, close_time, open_price, close_price, high_price, low_price, is_interval_end, sma_calculated, stddev_calculated, band_higher, band_lower, buy_or_sell])
                file_r.close()
                print(len(csvreader_r))

    file_read.close()
    file_read_r.close()


# async def time_conversion(start_time_unix, close_time_unix):
#     start_time = datetime.fromtimestamp(start_time_unix)
#     close_time = datetime.fromtimestamp(close_time_unix)

#     return start_time, close_time
#  csvreader['SMA'][-1] = csvreader[-periods - 1:]['close_price'].rolling(window=20).mean()
