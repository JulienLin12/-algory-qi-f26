"""Homework 2 starter — Algory QI Education, Fall 2026

Fill in every function marked TODO. Do not rename them: the checker looks for
these exact names. Run `python check_hw02.py` before you submit.
"""
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------- Q1
def present_value(cash_flows, rate):
    """Present value of a list of cash flows, the first arriving in one year.

    present_value([10, 15, 20], 0.10) -> 36.51
    """
    # TODO
    counter = 0
    result = 0
    for years in cash_flows:
        result += cash_flows[counter] /((1 + rate) ** (counter + 1))
        counter += 1
    return result


#print(present_value([10, 15, 20], 0.10))


# ---------------------------------------------------------------- Q2
def bond_price(face, coupon_rate, years, market_rate):
    """Price of a bond paying an annual coupon and repaying face at maturity.

    The final year pays the coupon AND the face value. That is the usual bug.
    bond_price(1000, 0.04, 10, 0.04) -> exactly 1000.0
    """
    # TODO 
    yearly_payment = coupon_rate * face
    cash_flows = []

    for year in range(years):
        cash_flows.append(yearly_payment)

    cash_flows[-1] += face

    return round(present_value(cash_flows, market_rate), 2)

print(bond_price(1000, 0.04, 10, 0.04))

# ---------------------------------------------------------------- Q4/Q5
def annualised_return(prices):
    """Annualised return from a price series, using 252 trading days."""
    # TODO
    prices = pd.Series(prices, dtype=float)
    prices = prices.dropna()

    total_growth = prices.iloc[-1] / prices.iloc[0]
    number_of_returns = len(prices) - 1

    return total_growth ** (252 / number_of_returns) - 1


def annualised_volatility(prices):
    """Annualised standard deviation of daily returns."""
    # TODO
    prices = pd.Series(prices, dtype=float)
    daily_returns = prices.pct_change(fill_method=None).dropna()

    return daily_returns.std() * np.sqrt(252)


def beta(stock_prices, market_prices):
    """Beta of a stock against the market.

    Covariance of the two RETURN series divided by the variance of the market's.
    Computing this on prices instead of returns is a common and silent error.
    beta(spy, spy) -> 1.0
    """
    # TODO
    stock_prices = pd.Series(stock_prices, dtype=float)
    market_prices = pd.Series(market_prices, dtype=float)
    stock_returns = stock_prices.pct_change(fill_method=None)
    market_returns = market_prices.pct_change(fill_method=None)

    # Match dates and keep only days with both returns
    returns = pd.concat(
        [stock_returns, market_returns],
        axis=1
    )
    returns.columns = ["stock", "market"]
    returns = returns.dropna()

    covariance = returns["stock"].cov(returns["market"])
    market_variance = returns["market"].var()

    return covariance / market_variance


# ---------------------------------------------------------------- your answers
def main():
    """Everything the assignment asks you to print goes here."""
    print("Q1  present_value([10, 15, 20], 0.10) =", present_value([10, 15, 20], 0.10))
    # TODO: Q3 — three bond prices, then the price-vs-rate plot
    for rate in [0.02, 0.04, 0.0496]:
        price = bond_price(1000, 0.04, 10, rate)
        print(f"Market rate {rate:.2%}: ${price:,.2f}")

    rates = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05,
             0.06, 0.07, 0.08, 0.09, 0.10]

    prices = []
    percentages = []

    for rate in rates:
        price = bond_price(1000, 0.04, 10, rate)
        prices.append(price)
        percentages.append(rate * 100)

    plt.plot(percentages, prices)
    plt.xlabel("Market rate (%)")
    plt.ylabel("Bond price ($)")
    plt.title("10-year bond with a 4% coupon")
    plt.grid(True)
    plt.show()

    # TODO: Q4 — download your three tickers and SPY, print trading days for each
    tickers = ["7974.T", "SGE.L", "AAPL", "SPY"]

    data = yf.download(
        tickers,
        period="5y",
        interval="1d",
        auto_adjust=False,
        progress=False
    )

    closing_prices = data["Close"]

    for ticker in tickers:
        prices = closing_prices[ticker].dropna()
        print(f"{ticker}: {len(prices)} trading days")
    # TODO: Q5 — the table of return, volatility and beta
    results = []

    for ticker in tickers:
        prices = closing_prices[ticker]

        results.append({
            "Ticker": ticker,
            "Return": annualised_return(prices),
            "Volatility": annualised_volatility(prices),
            "Beta": beta(prices, closing_prices["SPY"])
        })

    table = pd.DataFrame(results)

    print(table.to_string(
        index=False,
        formatters={
            "Return": "{:.2%}".format,
            "Volatility": "{:.2%}".format,
            "Beta": "{:.2f}".format
        }
    ))
    # TODO: Q6 — both rankings
        # Print the three prices
    for rate in [0.02, 0.04, 0.0496]:
        price = bond_price(1000, 0.04, 10, rate)
        print(f"Market rate {rate:.2%}: ${price:,.2f}")

    # Calculate prices across 0% to 10%
    percentages = []
    prices = []

    for i in range(101):
        percentage = i / 10       # 0, 0.1, 0.2, ... 10%
        rate = percentage / 100  # Convert percentage to decimal

        percentages.append(percentage)
        prices.append(bond_price(1000, 0.04, 10, rate))

    plt.plot(percentages, prices)
    plt.xlabel("Market rate (%)")
    plt.ylabel("Bond price ($)")
    plt.title("10-year bond with a 4% coupon")
    plt.grid(True)
    plt.show()

    print(
        "The curve'a slope is facing downward and tend to bend upward. We call this convexity. "
        "This happens because the bond gains more when rates fall than it loses when rates"
        "rise by the same amount."
    )


if __name__ == "__main__":
    main()