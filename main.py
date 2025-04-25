import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel("mlb-odds-2021.xlsx")
#Note that, for even n, the nth + 1 team was their opponent
data = df.filter(["Date","Final", "Open"],axis=1)
for year in range(2010,2020):
    temp_data = pd.read_excel("mlb-odds-" + str(year) + ".xlsx")
    temp_data = df.filter(["Date","Final", "Open"],axis=1)
    data = pd.concat([data, temp_data])
    print("Loading data from ", str(year))
print(data.info())

profit_fav = [0]
profit_und = [0]
prev_date = data.iloc[0,0]
day_games = 0
for i in range(int(len(data)/2)):
    day_games += 1
    last_index = len(profit_und) - 1
    t1odd = data.iloc[2*i, 2]
    t2odd = data.iloc[2*i + 1, 2]
    #case that team 1 wins
    if data.iloc[2*i,1] > data.iloc[2*i + 1,1]:
        if t1odd > 0: #t1 is the underdog
            profit_und[last_index] += t1odd
            profit_fav[last_index] -= 100
        else: #t1 was the favorite
            profit_fav[last_index] -= 10000 / t1odd #subtract due to negative sign
            profit_und[last_index] -= 100
    else:
        if t2odd > 0: #t2 is the underdog
            profit_und[last_index] += t2odd
            profit_fav[last_index] -= 100
        else: #t2 was the favorite
            profit_fav[last_index] -= 10000 / t2odd #subtract due to negative sign
            profit_und[last_index] -= 100
    if data.iloc[2*i+1,0] != prev_date:
        prev_date = data.iloc[2*i+1,0]
        profit_fav[last_index] /= day_games
        profit_und[last_index] /= day_games
        profit_fav.append(0)
        profit_und.append(0)
        day_games = 0


plt.figure()
plt.hist(profit_fav, color="red",bins=40,label="Betting on the favorite",alpha=.80)
plt.hist(profit_und, color="blue",bins=40,label="Betting on the underdog",alpha=.80)
plt.title("Frequency of profit in 2021 season")
plt.legend()
plt.savefig("ee24finalprojectplot1")
