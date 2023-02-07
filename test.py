from datetime import datetime, timezone
import pandas as pd
import csv
periods = 20

print('ga')
with open("currency_info.csv", "r") as file:
    csvreader = pd.read_csv(file)
    if len(csvreader) >= periods + 1:
        print("Proceed calculating Bollinger Bands...")
        # with open('currency_info.csv', 'a', newline='') as file:
        #     writing = csv.writer(file)
        sma_calculated = csvreader[-periods -
                                   1:]['close_price'].rolling(window=20).mean()

        print("The calculated SMA: ", sma_calculated)
        print("Type SMA: ", type(sma_calculated))
        print("len csv periods: ", len(
            csvreader[-periods - 1:]['close_price']))
        print("content csv periods: ", (
            csvreader[-periods - 1:]['close_price']))
        print("type csv periods: ", type(
            csvreader[-periods - 1:]['close_price']))
        print("type csv periods: ", type(
            csvreader[-periods - 1:]['close_price'].to_frame()))
        print("Rolling(): ", csvreader[-periods - 1:]
              ['close_price'].rolling(window=20))

        print("sma: ", csvreader[-periods -
                                 1:]['close_price'].rolling(window=20).mean().loc[-1])
