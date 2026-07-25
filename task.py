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

