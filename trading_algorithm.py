import yfinance as yf
import pandas as pd

ticker = "COFF.L"
short_window = 20
long_window = 50

data = yf.download(ticker, start="2021-01-01", end="2026-07-25",
                   auto_adjust=False)

data.columns = data.columns.get_level_values(0)
data = data[["Open", "High", "Low", "Close", "Volume"]]
coffe_df = pd.DataFrame(data)
coffe_df = coffe_df.dropna()

print(coffe_df.head())