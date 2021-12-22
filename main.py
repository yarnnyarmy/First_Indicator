import pandas as pd
import MetaTrader5 as mt5
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# initialize MetaTrader 5
if mt5.initialize():
    print("Initialization successful")
else:
    print("Initialization unsuccessful")
    mt5.shutdown()


login = 6048029
password = 'yxzgltu0'
server = 'OANDA-OGM MT5 Demo'

mt5.login(login, password, server)

# login credentials

login = 6048029
password = 'yxzgltu0'
server = 'OANDA-OGM MT5 Demo'

credentials = mt5.login(login, password, server)

if credentials:
    accountInfo = mt5.account_info()
    if accountInfo is not None:
        account_info_dict = mt5.account_info()._asdict()
        df = pd.DataFrame(list(account_info_dict.items()), columns=['property', 'value'])
        print("account_info() as dataframe:")
        print(df)
else:
    print("Connection failed", mt5.last_error())

# Get the first 1000 bars, of the 1 HR time frame from EURUSD


rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_H1, 0, 1000)

# display each element of obtained data in a new line
print("Display obtained data 'as is'")
for rate in rates:
    print(rate)

# create DataFrame out of the obtained data
df = pd.DataFrame(rates)
# convert time in seconds into the datetime format
df['time'] = pd.to_datetime(df['time'], unit='s')

# display data
print("\nDisplay dataframe with data")
print(df)

# function for finding trend line up
# if the middle is higher than the first two bars and the last two bars, then it is a fractal


def uptrend(df1, n2, n1):
    for i in range(n2, n1-3):
        if df1.high[i] < df1.high[i+1]:
            break
        if df1.high[i] < df1.high[i+2]:
            break
        if df1.high[i] < df1.high[i-1]:
            break
        if df1.high[i] < df1.high[i-2]:
            break
        return True
    return False


# look for another fractal that is lower than the previous fractal that was found
# if the fractal has the same time as the first fractal break out the loop


def uptrend2(df2, n3, n4):
    for a in range(n3, n4 - 3):
        if df2.high[a] > frac1[0][1]:
            break
        if df2.time[a] == frac1[0][2]:
            break
        if df2.high[a] < df2.high[a + 1]:
            break
        if df2.high[a] < df2.high[a + 2]:
            break
        if df2.high[a] < df2.high[a - 1]:
            break
        if df2.high[a] < df2.high[a - 2]:
            break
        return True
    return False

# two list for the fractals we found


frac1 = []
frac2 = []
# count three bars before the find the first fractal and leave space for 7 bars to the end


n1 = 3
n2 = 7

# looking through 1000 bars
e = 1000

# loop to add the fractals to the frac1 list
# for the row in the range of 3-7
# if row is less that 1000-7
# add the row number, the high price of the bar, and the time of the bar


for row in range(n1, e+n1):
    if uptrend(df, row, e):
        if row < e-n2:
            frac1.append((row, df.high[row], df.time[row]))

# for loop to add elements to the second list that are lower than the first fractal
for row in range(n1, e+n1):
    if uptrend2(df, row, e):
        if row < e-n2:
            frac2.append((row, df.high[row], df.time[row]))

# print the length of the list and all the elements


print("The fractals for 1 are ", len(frac1))
print(frac1)
print("The fractals for 2 are ", len(frac2))
print(frac2)
