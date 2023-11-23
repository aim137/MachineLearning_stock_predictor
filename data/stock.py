import yfinance as yf
from datetime import datetime

def get_stock_data(ticker,start_date = None, end_date = None):
    """
    Gets daily data for a stock and returns a pandas df with date and Close value.
    If either date is None, will use yfinance.download defaults
    """
    
    if isinstance(start_date,datetime) and isinstance(end_date,datetime):
        _data = yf.download(ticker,start = start_date, end = end_date)
    else:
        _data = yf.download(ticker)

    _data.reset_index(inplace=True)
    _data = _data[["Date","Close"]]
    
    return _data



if __name__ == "__main__":
    df = get_stock_data('TSLA')
    print(df)
