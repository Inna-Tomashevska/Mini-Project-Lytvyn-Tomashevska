import yfinance as yf

ticker = "COFF.L"
short_window = 20
long_window = 50

data = yf.download(ticker, start="2021-01-01", end="2026-07-25",
                   auto_adjust=False)

data.columns = data.columns.get_level_values(0)

data = data[["Close", "High", "Low", "Open", "Volume"]]

print(data.head())
print(data.tail())
print(data.columns)
print(data.shape)