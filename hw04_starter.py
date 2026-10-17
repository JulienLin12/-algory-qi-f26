"""Homework 4 starter — Algory QI Education, Fall 2026

The backtester is the piece worth getting right. Everything after it in the
semester assumes it works.
"""
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

LOOKBACK = 60
data = yf.download(
        "^SP500TR",
        start="1990-01-01",
        auto_adjust=False,
        progress=False,
    )
prices = data["Close"]
prices_series = data["Close"].squeeze()


# ---------------------------------------------------------------- Q1
def load_and_split(split_date="2011-09-09", prices=None, warmup=LOOKBACK):
    """Split ^SP500TR since 1990 into training and test at `split_date`.

    Training ends on the split date's close. Test begins `warmup` trading days
    BEFORE it, so the 60-day window is already full on the first day traded out
    of sample. Those overlapping days are history the strategy reads, never days
    it earns a return on. Cut the series at one date with no overlap and the
    first 60 days of the test set have no window, so the out-of-sample period
    silently starts three months late.

    September 9, 2011 is a Friday. A split date has to be a trading day, or
    "ends on that close" names a close that does not exist.

    Pass `prices` to split a series you already have, which is how the checker
    tests this without a download. Return (training, test).
    """
    
    if split_date not in data.index:
     return "The date chosen is not a trading day, please choose a trading day"
    
    training = data.loc["1990-01-01":split_date]
    test = data.loc[split_date:]
    print("Training length:", len(training))
    print("Training mean closing price:", training["Close"].mean().iloc[0])

    print("Test length:", len(test))
    print("Test mean closing price:", test["Close"].mean().iloc[0])
    return training, test




# ---------------------------------------------------------------- Q2, Q4, Q5
def always_hold(window):
    """Always invest. The control case, and the one that proves the backtester."""
    return True


def always_cash(window):
    """Never invest. Must produce exactly 0% return."""
    return False


def make_random_hold(p=0.7, seed=0):
    """Return a strategy that invests with probability p each day.

    A factory, not a plain function, because the generator has to live somewhere
    and a default argument is the wrong place: `rng=np.random.default_rng(0)` in
    a signature is evaluated once when the module loads, so every backtest in the
    session shares one advancing generator and the same backtest returns a
    different number each time you run it. Building the generator here gives one
    per strategy, so `backtest(train, make_random_hold())` is reproducible.
    """
    rng = np.random.default_rng(seed)

    def random_hold(window):
        return bool(rng.random() < p)

    return random_hold


def five_day_reversal(window):
    """The rule from class: hold unless the last 5 days were positive.

    Measure that return from the close 5 days before today to today's close,
    both of which are inside the window.
    """
    position = False
    for i in range(5):
        if (window.iloc[-(i+2)]- window.iloc[-(i+1)]) < 0:
            position = True
    return position
    
def three_day_reversal(window):
    """The rule from class: hold unless the last 5 days were positive.

    Measure that return from the close 5 days before today to today's close,
    both of which are inside the window.
    """
    position = False
    for i in range(3):
        if (window.iloc[-(i+2)]- window.iloc[-(i+1)]) > 0:
            position = True
    return position

def my_strategy(window):
    """Your own rule. It sees only `window`, the previous LOOKBACK closes.

    It must never look at anything after that. That is the whole assignment.
    """
    return three_day_reversal(window)

def five_days_average_and_three_day_reversal(window):
    """Your own rule. It sees only `window`, the previous LOOKBACK closes.

    It must never look at anything after that. That is the whole assignment.
    """
    if three_day_reversal and five_days_average(window) == True:
        return True
    else:
        return False
def ten_days_average(window):
    """Your own rule. It sees only `window`, the previous LOOKBACK closes.

    It must never look at anything after that. That is the whole assignment.
    """
    ten_days_average = 0
    for i in range(10):
        ten_days_average += window.iloc[-(i+1)]
    ten_days_average = ten_days_average / 10
    if window.iloc[-1] > ten_days_average:
        return True
    else:
        return False

def five_days_average(window):
    """Your own rule. It sees only `window`, the previous LOOKBACK closes.

    It must never look at anything after that. That is the whole assignment.
    """
    five_days_average = 0
    for i in range(5):
        five_days_average += window.iloc[-(i+1)]
    five_days_average = five_days_average / 5
    if window.iloc[-1] > five_days_average:
        return True
    else:
        return False

# ---------------------------------------------------------------- Q3
def backtest(prices, strategy, lookback=LOOKBACK):
    """Walk forward one day at a time and apply the strategy's decision.

    The convention, stated exactly, because everything else depends on it:

        on day i, the strategy is handed prices[i - lookback + 1 : i + 1],
        the `lookback` closes ENDING WITH today's, today's included;
        if it says hold you earn prices[i + 1] / prices[i] - 1, otherwise zero.

    So i runs from lookback - 1 to len(prices) - 2. The first decision is made on
    the 60th close and the first return earned runs from the 60th close to the
    61st. Today's close is known when you decide, so withholding it throws away a
    day of information for nothing; tomorrow's close is what you are predicting,
    so reading it is the bug this whole session is about.

    Return a dict with at least:
        total_return, annualised_return, max_drawdown, fraction_invested

    Annualise by trading days, 252 a year, compounded: value ** (252 / days) - 1.

    Sanity checks before you trust it:
        always_hold  must match buy-and-hold over the days actually traded,
                     prices[-1] / prices[lookback - 1] - 1, not over the
                     whole file
        always_cash  must return exactly 0.0
    If either fails you have an off-by-one, and every number after it is fiction.
    """
    prices_series = prices["Close"].squeeze()
    portfolio_value = 1
    portfolio_value_tracker = []
    peak_value = 1.0
    max_drawdown = 0.0
    count = 0
    total_count = 0
    for i in range(lookback - 1, len(prices_series) - 1):
        total_count += 1
        lookback_prices = prices_series[i - lookback + 1 : i + 1]
        if strategy(lookback_prices) == True:
            daily_return = prices_series.iloc[i + 1] / prices_series.iloc[i] - 1
            count += 1
        else:
            daily_return = 0
        portfolio_value *= (1 + daily_return)
        peak_value = max(peak_value, portfolio_value)
        current_drawdown = portfolio_value / peak_value - 1
        max_drawdown = min(max_drawdown, current_drawdown)
        portfolio_value_tracker.append(portfolio_value)

    print('total_return', portfolio_value)
    print('annualised_return', portfolio_value ** (252 / total_count) - 1)
    print('max_drawdown', max_drawdown)
    print('fraction_invested', count/total_count)

    portfolio_value_index = 1
    portfolio_value_index_tracker = []

    for i in range(lookback - 1, len(prices_series) - 1):
        daily_return = prices_series.iloc[i + 1] / prices_series.iloc[i] - 1
        portfolio_value_index *= 1 + daily_return
        portfolio_value_index_tracker.append(portfolio_value_index)

    dates = prices_series.index[lookback:]

    plt.figure()

    plt.plot(
        dates,
        portfolio_value_tracker,
        label="My strategy",
        color="blue",
        linewidth=3,
    )

    plt.plot(
        dates,
        portfolio_value_index_tracker,
        label="Buy and hold",
        color="orange",
        linestyle="--",
        linewidth=1.5,
    )

    plt.xlabel("Time")
    plt.ylabel("Value of an initial investment of 1")
    plt.legend()
    plt.grid(True)
    plt.show()
    return {
        "total_return": portfolio_value - 1,
        "annualised_return": portfolio_value ** (252 / total_count) - 1,
        "max_drawdown": max_drawdown,
        "fraction_invested": count / total_count,
    }

def main():
    train, test = load_and_split()
    #backtest(train, always_hold, 60)
    #for name, strat in [("always hold", always_hold),
    #                   ("always cash", always_cash),
    #                    ("random 70%", make_random_hold(0.7, seed=0)),
    #                    ("5-day reversal", five_day_reversal),
    #                    ("10 days average", ten_days_average),
    #                    ("three days reversal", three_day_reversal),
    #                    ("5-day reversal", five_day_reversal),                                                     
    #                    ("my strategy", my_strategy)]:
    #    r = backtest(train, strat)
    #    print(f"{name:<16} total {r['total_return']:+.1%}   annual {r['annualised_return']:+.2%}")
    r = backtest(train, my_strategy)
    r = backtest(test, my_strategy)
    if three_day_reversal(prices_series.iloc[-60:]) == True:
        print("My stragety's position for today: hold")
    else:
        print("My stragety's position for today: cash")
    # r = backtest(test, always_hold)
    # TODO: Q6 — print EVERY variant you try, not just the one you keep
    # TODO: Q8 — run my_strategy on the test set. Once.a
    # TODO: Q9 — what does your rule say to do today?


if __name__ == "__main__":
    main()