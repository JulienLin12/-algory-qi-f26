"""Homework 3 starter — Algory QI Education, Fall 2026

Fill in every function marked TODO. Keep the names: the checker looks for them.
Run `python check_hw03.py` as you go.
"""
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import random

spy = yf.download(
        "SPY",
        period="10y",
        interval="1d",
        auto_adjust=False,
        multi_level_index=False,
        progress=False
)

closes = spy["Close"].dropna()
returns = closes.pct_change(fill_method=None).dropna()
average_returns = returns.mean()
print("Number of trading days:", len(closes))
print("Number of daily returns:", len(returns))
print("Mean daily return:", average_returns)
# ---------------------------------------------------------------- Q1
def simulate_dice(trials, seed=0):
    """Pick a 4-sided or 6-sided die at random, roll it, repeat.

    Return the estimated P(picked the 4-sided die | rolled a 1).
    The exact answer is 0.6. Take a seed so your result is reproducible.
    """
    random.seed(seed)
    dice1 = 0
    dice2 = 0
    Score1 = [0, 0, 0, 0, 0, 0]
    Score2 = [0, 0, 0, 0, 0, 0]
    for i  in range(trials):
        dice = random.randint(1,2)
        if dice == 1:
            dice1 += 1
            Score1[random.randint(1,4) - 1] += 1
        elif dice == 2:
            dice2 += 1
            Score2[random.randint(1,6) - 1] += 1
    print("dice1:",  dice1)
    print("dice2:",  dice2)
    print("Score1:",  Score1)
    print("Score2:", Score2)
    probability = (Score1[0])/(Score1[0] + Score2[0])
    return probability



# ---------------------------------------------------------------- Q2
def simulate_coins(trials, seed=0):
    """Flip three fair coins, get paid (heads x tails). Return the mean payout.

    The exact answer is 1.5.
    """
    random.seed(seed)
    pay = 0
    for i in range(trials):
        heads = 0
        tails = 0
        for i in range(3):
                 result = random.randint(1,2)
                 if result == 1:
                     heads += 1
                 elif result == 2:
                     tails += 1
        pay += heads * tails
    return (pay/trials)




# ---------------------------------------------------------------- Q5/Q6
def p_down(returns):
    """Fraction of days with a negative return. Count them yourself."""
    true_case = 0
    case = 0
    for i in range(len(returns)):
        case += 1
        if returns.iloc[i] < 0:
            true_case += 1
    print("case:", case)
    print("true_case:", true_case)
    return (true_case/case)


def p_down_given_down(returns):
    """P(tomorrow is down | today was down), counted directly from the series."""
    case = 0
    true_case = 0
    flag = False
    for i in range(len(returns) - 1):
        if returns.iloc[i] < 0:
            case += 1
            if returns.iloc[i + 1] < 0:
                flag = True
            else:
                flag = False
        else:
            flag = False
        if flag == True:
            true_case += 1
    print("case:", case)
    print("true_case:", true_case)
    return (true_case/case)


def p_down_given_big_drop(returns, threshold=-0.02):
    """P(tomorrow is down | today fell more than the threshold).

    Also report how many days the estimate uses. A handful of days is a much
    weaker claim than thousands, and the count is what tells a reader which of
    the two this is.
    """
    case = 0
    true_case = 0
    flag = False
    for i in range(len(returns) - 1):
        if returns.iloc[i] < threshold:
            case += 1
            if returns.iloc[i + 1] < 0:
                flag = True
            else:
                flag = False
        else:
            flag = False
        if flag == True:
             true_case += 1
    print("case:", case)
    print("true_case:", true_case)
    return (true_case/case)
    


# ---------------------------------------------------------------- Q7
def expected_present_value(cash_flows, rate, survival_prob):
    """Present value where the company survives EACH year with survival_prob.

    Year 1 is certain. Year 2 arrives with probability survival_prob, year 3
    with survival_prob squared, and so on. This is a yearly hazard rate.

    Note this is deliberately more general than the Session 3 slide, which had a
    single shutdown event after year 1 and came to 16.98. A yearly 50% survival
    is a harsher assumption and gives 15.10. Getting 16.98 here means you applied
    the probability once instead of compounding it.
    """
    counter = 0
    result = 0
    
    for years in cash_flows:
        result += cash_flows[counter]*survival_prob**counter /((1 + rate) ** (counter + 1))
        counter += 1
    return result



def main():
    # print("Q1  P(4-sided | rolled a 1) =", simulate_dice(100000, 49))
    # print("Q2  expected three-coin payout =", simulate_coins(100000, 49))
    #trials = [100, 1000, 10000, 100000]
    # results = [0, 0, 0, 0]
    # for i in range(4):
    #    results[i] = simulate_coins(trials[i], 49)
    # plt.plot(trials, results, marker="o", label="Simulated payout")
    # plt.axhline(y=1.5, color="red", linestyle="--", label="Exact answer: 1.5")

    # plt.xscale("log")
    # plt.xlabel("Number of trials")
    # plt.ylabel("Expected payout")
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    # print("p_down :", p_down(returns))
    # print("p_down_given_down :", p_down_given_down(returns))
    # print("probability down_given_big_drop :", p_down_given_big_drop(returns))
    # print("Q7  EPV =", expected_present_value([10, 10, 10], 0.10, 0.5))

    if __name__ == "__main__":
        main()