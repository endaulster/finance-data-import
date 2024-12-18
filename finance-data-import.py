import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

# %matplotlib inline
import seaborn as sns
import yfinance as yf

# The user is able to write his ticker symbol in the terminal, so we make a basic "interface"
os.system('clear') 
print("Finance Data Importer 0.1")
print("")
print("This basic tool will help you download financial statements of the required ticker")
print("")
input("Press Enter to continue...")

os.system('clear') 
print("Finance Data Importer 0.1")
print("")

ticker_input = input("Write your ticker symbol: ")

os.system('clear') 
print("Finance Data Importer 0.1")
print("")
print("Working...")
print("")
print("Be patient")
ticker_symbol = ticker_input.upper()
ticker = yf.Ticker(ticker_symbol)

# We import the whole data from that symbol

WStockInfo = ticker.info
WIncomeStmt = ticker.financials 
WBalanceSheet = ticker.balance_sheet
WCashFlow = ticker.cash_flow

# We give format to the stock main info
StockInfo = pd.DataFrame(WStockInfo.items(), columns=['Key', 'Value'])

# For some reason, the information is upside down so we fix it
UIncomeStmt = WIncomeStmt.iloc[::-1]
UBalanceSheet = WBalanceSheet.iloc[::-1]
UCashFlow = WCashFlow.iloc[::-1]

# We are gonna export these numbers in thousands, so we have to make exceptions 
exclude_rows = ['Basic EPS', 'Diluted EPS']

# We then loop through until we polished our information
def divide_by_thousands (df, exclude_rows=[]):
    df_divided = df.copy()
    for row in df_divided.index:
        if row not in exclude_rows:  # Exclude specific rows (e.g., 'Basic EPS', 'Diluted EPS')
            df_divided.loc[row] = df_divided.loc[row] / 1000
    return df_divided

IncomeStmt = divide_by_thousands(UIncomeStmt, exclude_rows)
BalanceSheet = divide_by_thousands(UBalanceSheet)
CashFlow = divide_by_thousands(UCashFlow)

# We set the path of the exported file and put a name to it
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
file_path = os.path.join(downloads_path, f"{ticker_symbol}_data.xlsx")

# Export it
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    StockInfo.to_excel(writer, sheet_name="Stock Info")
    IncomeStmt.to_excel(writer, sheet_name="Income Statement")
    BalanceSheet.to_excel(writer, sheet_name="Balance Sheet")
    CashFlow.to_excel(writer, sheet_name="Cash Flow")

# Done!

os.system('clear') 
print("Finance Data Importer 0.1")
print("")
print(f"{ticker_symbol} information was exported successfully")
print("")
input("Press Enter to exit...")
os.system('clear') 