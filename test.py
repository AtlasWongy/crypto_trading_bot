from datetime import datetime, timezone
import pandas as pd
import csv
with open('currency_info.csv', 'a', newline='') as file, open('bollinger_band.csv', 'a', newline='') as file_r:
    writing = csv.writer(file)
    writing_r = csv.writer(file_r)  # results file
    with open("currency_info.csv", "r") as file, open('bollinger_band.csv', "r") as file_r:
        csvreader = pd.read_csv(file)
        csvreader_r = pd.read_csv(file_r)
        # change to periods*interval_records_num?? enough for 20 5-min stick
        # and use is_interval_end to decide whether this candlestick is for the entire 5min
        kline_ind = csvreader.index[csvreader['is_interval_end']
                                    == False].tolist()
        # sell_ind = csvreader[periods+1:].index[csvreader['Buy/Sell']
        #                                   [periods+1:] == 'sell'].tolist()
        print(len(csvreader))
        print(type(len(csvreader)))
        kline_ind.append(len(csvreader))
        print(kline_ind)
        print(csvreader['close_price'][kline_ind])
