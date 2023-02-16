import matplotlib.pyplot as plt
import pandas as pd
import csv

# this plot to be changed
periods = 20
with open("bollinger_band.csv", "r") as file:
    csvreader = pd.read_csv(file)
    # , csvreader['SMA'],csvreader['Upper'], csvreader['Lower']
    # plt.plot(csvreader['close_price'], label="close_price")
    # plt.plot(float(csvreader['SMA']), label="SMA")
    # plt.plot(csvreader[['SMA', 'Upper']], label="SMA")
    ind = csvreader['Upper'].index
    upper = csvreader['Upper'] .astype(float)
    lower = csvreader['Lower'].astype(float)
    buy_ind = csvreader.index[csvreader['Buy/Sell']
                              == 'buy'].tolist()
    sell_ind = csvreader.index[csvreader['Buy/Sell']
                               == 'sell'].tolist()
    plt.plot(csvreader['SMA'].astype(float), label="SMA")
    plt.plot(csvreader['close_price']
             .astype(float), label="close_price")
    plt.plot(upper, label="Upper")
    plt.plot(lower, label="Lower")
    plt.fill_between(ind, upper, lower, color='grey', alpha=0.3)
    plt.scatter(buy_ind, csvreader['close_price']
                [buy_ind], marker='^', color='g')
    plt.scatter(sell_ind, csvreader['close_price']
                [sell_ind], marker='v', color='r')
    print(ind)
    # plt.scatter()
plt.legend()
plt.show()

file.close()
