import matplotlib.pyplot as plt
import pandas as pd
import csv

periods = 20
with open("currency_info.csv", "r") as file:
    csvreader = pd.read_csv(file)
    # , csvreader['SMA'],csvreader['Upper'], csvreader['Lower']
    # plt.plot(csvreader['close_price'], label="close_price")
    # plt.plot(float(csvreader['SMA']), label="SMA")
    # plt.plot(csvreader[['SMA', 'Upper']], label="SMA")
    df = csvreader['Upper'].index[periods+1:]
    print(csvreader['SMA'])
    print(csvreader.dtypes)
    ind = csvreader['Upper'].index[21:]
    upper = csvreader['Upper'][21:].astype(float)
    lower = csvreader['Lower'][21:].astype(float)
    buy_ind = csvreader[21:].index[csvreader['Buy/Sell']
                                   [21:] == 'buy'].tolist()
    sell_ind = csvreader[21:].index[csvreader['Buy/Sell']
                                    [21:] == 'sell'].tolist()
    plt.plot(csvreader['SMA'][21:].astype(float), label="SMA")
    plt.plot(csvreader['close_price'][21:].astype(float), label="close_price")
    plt.plot(upper, label="Upper")
    plt.plot(lower, label="Lower")
    plt.fill_between(ind, upper, lower, color='grey', alpha=0.3)
    plt.scatter(buy_ind, csvreader['close_price']
                [buy_ind], marker='^', color='g')
    plt.scatter(sell_ind, csvreader['close_price']
                [sell_ind], marker='v', color='r')
    print(buy_ind)
    # plt.scatter()
plt.legend()
plt.show()

file.close()
