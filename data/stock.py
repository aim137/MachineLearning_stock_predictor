import yfinance as yf
from datetime import datetime
from pandas.core.frame import DataFrame

def get_stock_data(ticker: str,start_date:str = None, end_date:str = None) -> DataFrame:
    """
    Gets daily data for a stock and returns a pandas df with date and Close value.
    If either date is None, will use yfinance.download defaults
    Dates should be in the format 'YYYYMMDD', e.g., '20220202'
    """
    
    start, end = get_dates(start_date,end_date)
    try:
        _data = yf.download(ticker,start = start, end = end)
    except:
        _data = yf.download(ticker)

    _data.reset_index(inplace=True)
    _data = _data[["Date","Close"]]
    
    return _data


def get_dates(s,e):
    try:
        _start = datetime.strptime(s,'%Y%m%d')
    except:
        _start = datetime(2000,1,1)
    try:
        _end = datetime.strptime(e,'%Y%m%d')
    except:
        _end = datetime.today()
    return _start, _end

if __name__ == "__main__":
    df = get_stock_data('TSLA')
    print(df)
