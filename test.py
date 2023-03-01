from datetime import datetime, timezone
import pandas as pd
import csv
with open('csv/currency_info.csv', 'a', newline='') as file, open('csv/bollinger_band.csv', 'a', newline='') as file_r:
    writing = csv.writer(file)
    writing_r = csv.writer(file_r)  # results file
    with open("csv/currency_info.csv", "r") as file, open('csv/bollinger_band.csv', "r") as file_r:
        csvreader = pd.read_csv(file)
        csvreader_r = pd.read_csv(file_r)
        # change to periods*interval_records_num?? enough for 20 5-min stick
        # and use is_interval_end to decide whether this candlestick is for the entire 5min
        kline_ind = csvreader.index[csvreader['is_interval_end']
                                    == True].tolist()
        # sell_ind = csvreader[periods+1:].index[csvreader['Buy/Sell']
        #                                   [periods+1:] == 'sell'].tolist()
        periods = 2
        print(kline_ind[-periods:])
        print(kline_ind)
