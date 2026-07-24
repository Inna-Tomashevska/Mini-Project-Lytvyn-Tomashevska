import yfinance as yf
import pandas as pd

ticker = "COFF.L"
short_window = 20
long_window = 50

data = yf.download(ticker, start="2021-01-01", end="2026-07-25",
                   auto_adjust=False)

data.columns = data.columns.get_level_values(0)
data = data[["Open", "High", "Low", "Close", "Volume"]]
coffee_df = pd.DataFrame(data)
coffee_df = coffee_df.dropna()


coffee_df["20d_Av"] = coffee_df["Close"].rolling(short_window).mean()
coffee_df["50d_Av"] = coffee_df["Close"].rolling(long_window).mean()

print(coffee_df.tail())