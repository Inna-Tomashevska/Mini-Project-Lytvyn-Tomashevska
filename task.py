import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker = "COFF.L"
short_window = 20
long_window = 50

data = yf.download(ticker, start="2021-01-01", end="2026-07-25", auto_adjust=False)
data.columns = data.columns.get_level_values(0)
data = data[["Open", "High", "Low", "Close", "Volume"]]

coffee_df = pd.DataFrame(data)
coffee_df = coffee_df.dropna()

coffee_df["20d_Av"] = coffee_df["Close"].rolling(short_window).mean()
coffee_df["50d_Av"] = coffee_df["Close"].rolling(long_window).mean()

coffee_df["Signal"] = 0
coffee_df.loc[coffee_df["20d_Av"] > coffee_df["50d_Av"], "Signal"] = 1
coffee_df["Position"] = coffee_df["Signal"].diff()

actions = []
for position in coffee_df["Position"]:
    if position == 1:
        actions.append("BUY")
    elif position == -1:
        actions.append("SELL")
    else:
        actions.append("HOLD")
coffee_df["Action"] = actions


coffee_df["Market_Return"] = coffee_df["Close"].pct_change()
coffee_df["Strategy_Return"] = coffee_df["Market_Return"] * coffee_df["Signal"].shift(1)

coffee_df["Cumulative_Market_Return"] = (1 + coffee_df["Market_Return"]).cumprod()
coffee_df["Cumulative_Strategy_Return"] = (1 + coffee_df["Strategy_Return"]).cumprod()

total_market_return = coffee_df["Cumulative_Market_Return"].iloc[-1] - 1
total_strategy_return = coffee_df["Cumulative_Strategy_Return"].iloc[-1] - 1

print(f"Buy & Hold total return: {total_market_return:.2%}")
print(f"Strategy total return: {total_strategy_return:.2%}")

buy_signals = coffee_df[coffee_df["Position"] == 1]
sell_signals = coffee_df[coffee_df["Position"] == -1]

plt.figure(figsize=(14, 7))
plt.plot(coffee_df.index, coffee_df["Close"], label="Close Price", alpha=0.6)
plt.plot(coffee_df.index, coffee_df["20d_Av"], label="20-day MA")
plt.plot(coffee_df.index, coffee_df["50d_Av"], label="50-day MA")
plt.scatter(buy_signals.index, buy_signals["Close"], marker="^", color="green", s=100, label="BUY")
plt.scatter(sell_signals.index, sell_signals["Close"], marker="v", color="red", s=100, label="SELL")

plt.title("COFF.L — Moving Average Crossover Strategy")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()

plt.figure(figsize=(14, 6))
plt.plot(coffee_df.index, coffee_df["Cumulative_Market_Return"], label="Buy & Hold")
plt.plot(coffee_df.index, coffee_df["Cumulative_Strategy_Return"], label="MA Crossover Strategy")

plt.title("Cumulative Return: Strategy vs Buy & Hold")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.show()
