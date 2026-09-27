##Reminder: Remove the Window security smart app control

#5)The reason as to why Sage dropped by 7.74% on the 25th of April 2025 is because investors reacted
# to Donald Trump's tariffs. Sage is a company that proposes a software for accounting Indeed, around 40% of Sage's 
# generated revenue come from the US. Tariffs may affect the economy poorly. This may result in the company
# losing  customers, and thereby lower performances in revenues.

# 6)S&P500 largely outperformed Sage in 2025. However, I believe Sage to be underappreciated. Indeed, European
#countries such as France are progressively enforcing laws obligating companies to use softwares for accounting. 
# This gives a nice propect for future demand. While the market is scared that the company may be over taken by AI, Sage is proactively developping and 
# deploying AI tools.



print("Starting to run the program")
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

##Printing for sage values
data_sage = yf.download("SGE.L", start="2025-01-01", end="2026-01-01")
data_sage = data_sage.dropna()
close_sage = data_sage["Close"]
return_sage = close_sage.iloc[-1] - close_sage.iloc[0]
daily_returns_sage = close_sage.pct_change().dropna()
annualised_volatility_sage = daily_returns_sage.std() * np.sqrt(252)
biggest_move_date_sage = daily_returns_sage.abs().idxmax()
biggest_move_sage = daily_returns_sage.loc[biggest_move_date_sage]
print("Tick: SGE.L, Number of trading days: ", len(close_sage), 
      "\nLast price: ", close_sage.iloc[-1],
      "\nReturn profit: ", return_sage,
      "\nAnnualised volatility: ", annualised_volatility_sage,
      "\nBiggest move date: ", biggest_move_date_sage,"Price move value: ", biggest_move_sage)

##Printing for SPY values
data_spy = yf.download("SPY", start="2025-01-01", end="2026-01-01")
data_spy = data_spy.dropna()
close_spy = data_spy["Close"]
return_spy = close_spy.iloc[-1] - close_sage.iloc[0]
daily_returns_spy = close_spy.pct_change().dropna()
annualised_volatility_spy = daily_returns_spy.std() * np.sqrt(252)
biggest_move_date_spy = daily_returns_spy.abs().idxmax()
biggest_move_spy = daily_returns_spy.loc[biggest_move_date_spy]
print("Tick: SPY, Number of trading days: ", len(close_spy), 
      "\nFirst price: ", close_spy.iloc[0],
      "\nLast price: ", close_spy.iloc[-1],
      "\nAnnualised volatility: ", annualised_volatility_spy,
      "\nBiggest move date: ", biggest_move_date_spy,"Price move value: ", biggest_move_spy)

print("finished running the program")

rebased_sage = close_sage / close_sage.iloc[0] * 100
rebased_spy = close_spy / close_spy.iloc[0] * 100

plt.figure(figsize=(10, 5))
plt.plot(rebased_sage.index, rebased_sage, label="Sage (SGE.L)")
plt.plot(rebased_spy.index, rebased_spy, label="SPY")

plt.xlabel("Date")
plt.ylabel("Rebased price (starting value = 100)")
plt.title("Sage vs SPY")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

""" Outdated Code

1) testing the imports
import yfinance as yf, pandas as pd, numpy as np, matplotlib, sklearn
print('ok', len(yf.Ticker('AAPL').history(period='5d')), 'days pulled')

2) Printing the ticker, number of trading days, and first/last market price
##Printing for sage values
data_sage = yf.download("SGE.L", start="2025-01-01", end="2026-01-01")
data_sage = data_sage.dropna()
close_sage = data_sage["Close"]
print("Tick: SGE.L, Number of trading days: ", len(close_sage), 
      "\nFirst price: ", close_sage.iloc[0],
      "\nLast price: ", close_sage.iloc[len(close_sage)-1])

3) + 4)
##Printing for SPY values
data_spy = yf.download("SPY", start="2025-01-01", end="2026-01-01")
data_spy = data_spy.dropna()
close_spy = data_spy["Close"]
print("Tick: SPY, Number of trading days: ", len(close_sage), 
      "\nFirst price: ", close_spy.iloc[0],
      "\nLast price: ", close_spy.iloc[len(close_spy)-1])

print("finished running the program")

##Printing for sage values
data_sage = yf.download("SGE.L", start="2025-01-01", end="2026-01-01")
data_sage = data_sage.dropna()
close_sage = data_sage["Close"]
return_sage = close_sage.iloc[-1] - close_sage.iloc[0]
daily_returns_sage = close_sage.pct_change().dropna()
annualised_volatility_sage = daily_returns_sage.std() * np.sqrt(252)
print("Tick: SGE.L, Number of trading days: ", len(close_sage), 
      "\nLast price: ", close_sage.iloc[-1],
      "\nReturn profit: ", return_sage,
      "\nAnnualised volatility: ", annualised_volatility_sage,)

##Printing for SPY values
data_spy = yf.download("SPY", start="2025-01-01", end="2026-01-01")
data_spy = data_spy.dropna()
close_spy = data_spy["Close"]
return_spy = close_spy.iloc[-1] - close_sage.iloc[0]
daily_returns_spy = close_spy.pct_change().dropna()
annualised_volatility_spy = daily_returns_spy.std() * np.sqrt(252)
print("Tick: SPY, Number of trading days: ", len(close_spy), 
      "\nFirst price: ", close_spy.iloc[0],
      "\nLast price: ", close_spy.iloc[-1],
      "\nAnnualised volatility: ", annualised_volatility_spy,)

print("finished running the program")

rebased_sage = close_sage / close_sage.iloc[0] * 100
rebased_spy = close_spy / close_spy.iloc[0] * 100

plt.figure(figsize=(10, 5))
plt.plot(rebased_sage.index, rebased_sage, label="Sage (SGE.L)")
plt.plot(rebased_spy.index, rebased_spy, label="SPY")

plt.xlabel("Date")
plt.ylabel("Rebased price (starting value = 100)")
plt.title("Sage vs SPY")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

"""
