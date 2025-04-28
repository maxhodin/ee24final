import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy.stats import norm

def fit_gaussian(dataset):
    mean = np.mean(dataset) #uses arithmetic mean formula
    print("mean: ", mean)
    var = np.var(dataset) #uses sum of difference of mean squares formula
    print("variance: ", var)
    x  = np.linspace(min(dataset), max(dataset), 2266)
    return norm.pdf(x, loc=mean, scale=math.sqrt(var))

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
            profit_und[last_index] += t1odd /100
            profit_fav[last_index] -= 1
        else: #t1 was the favorite
            profit_fav[last_index] -= 100 / t1odd #subtract due to negative sign
            profit_und[last_index] -= 1
    else:
        if t2odd > 0: #t2 is the underdog
            profit_und[last_index] += t2odd /100
            profit_fav[last_index] -= 1
        else: #t2 was the favorite
            profit_fav[last_index] -= 100 / t2odd #subtract due to negative sign
            profit_und[last_index] -= 1
    if data.iloc[2*i+1,0] != prev_date:
        prev_date = data.iloc[2*i+1,0]
        profit_fav[last_index] /= day_games
        profit_und[last_index] /= day_games
        profit_fav.append(0)
        profit_und.append(0)
        day_games = 0


plt.figure()    
fig, ax1 = plt.subplots()
ax1.hist(profit_fav, color="red",bins=40,label="Betting on the favorite",alpha=.80)
ax1.hist(profit_und, color="blue",bins=40,label="Betting on the underdog",alpha=.80)
ax2 = ax1.twinx()
x1 = np.linspace(min(profit_fav), max(profit_fav), 2266)
x2 = np.linspace(min(profit_und), max(profit_und), 2266)
ax2.plot(x1, fit_gaussian(profit_fav), label="Favorite Fit",color="red")
ax2.plot(x2, fit_gaussian(profit_und), label="Underdog Fit",color="blue")
ax1.set_title("Frequency of profit in 2010-2021 season")
ax1.set_xlabel("Expected profit per game bet on, daily")
ax1.set_xlim(-1, 2)
ax2.set_xlim(-1, 2)
ax1.legend()
ax2.legend(loc="upper left")
ax1.set_ylabel("Frequency")
ax2.set_ylabel("Probability Density")
plt.tight_layout()
plt.savefig("ee24finalprojectplot1")
