import yfinance as yf
from datetime import datetime,timedelta,date
from sqlalchemy import create_engine
import pandas as pd
from pytz import timezone
from icecream import ic

def get_stock_data(ticker: str,start_date:str = None, end_date:str = None) -> tuple:
    """
    Gets daily data for a stock and returns a pandas df with date and Close value.
    If either date is None, will use yfinance.download defaults
    Dates should be in the format 'YYYY-MM-DD', e.g., '2022-02-02'
    """
    
    in_dates, market_close = get_dates(start_date,end_date)

    _data, n_lines_pulled = update_write_db(ticker, in_dates)

    _data.reset_index(inplace=True)

    return _data[["Date","Close"]], in_dates, market_close, n_lines_pulled


def get_dates(s,e):
    try:
        _start = date.fromisoformat(s)
    except:
        _start = date(2000,1,1)
    while _start.weekday() > 4:
        _start += timedelta(days=1)

    try:
        _end = date.fromisoformat(e)
    except:
        _end = date.today()
    while _end.weekday() > 4:
        _end -= timedelta(days=1)

    # Avoid today if market still open
    if _end == date.today():
        market_close = datetime.now().astimezone(timezone('US/Eastern')).hour >= 16
        if not market_close:
            _end -= timedelta(days=1)
    else:
        market_close = True
    return (_start, _end), market_close

def update_write_db(ticker,in_dates):

    engine = create_engine(f'sqlite:///daily_data_stocks.db')

    # Update or create Table in DB
    with engine.connect() as connection:

        if engine.dialect.has_table(connection,f'{ticker}'):
            db_start = pd.read_sql(f'SELECT MIN(Date) from {ticker}',engine).values[0][0]
            db_end   = pd.read_sql(f'SELECT MAX(Date) from {ticker}',engine).values[0][0]
            db_start = date.fromisoformat(db_start.split(' ')[0])
            db_end   = date.fromisoformat(db_end.split(' ')[0])

            n_lines_pulled = 0

            if (in_dates[0] < db_start): 
                _data = yf.download(ticker,start = in_dates[0], end = db_start)
                _data.to_sql(f'{ticker}',engine, if_exists='append')
                n_lines_pulled += len(_data)

            if (in_dates[1] > db_end): 
                _data = yf.download(ticker,start = db_end + timedelta(days=1), end = in_dates[1]+timedelta(days=1))
                _data.to_sql(f'{ticker}',engine, if_exists='append')
                n_lines_pulled += len(_data)

        else:
            _data = yf.download(ticker,start = in_dates[0], end = in_dates[1])
            _data.to_sql(f'{ticker}',engine)
            n_lines_pulled = len(_data)
            return _data, n_lines_pulled # return df if Table in DB was created

    # Get data from DB
    _d1 = in_dates[0].isoformat()
    _d2 = (in_dates[1]+timedelta(days=1)).isoformat()
    _data = pd.read_sql(f"SELECT * FROM {ticker} WHERE Date BETWEEN '{_d1}' AND '{_d2}'",engine)
    _data.Date = pd.to_datetime(_data.Date)
    return _data, n_lines_pulled

if __name__ == "__main__":
    df = get_stock_data('TSLA','20201127','20201212')
    print(df)
    print(type(df.Date[0]))
    dd = get_stock_data('TSLA','20201127','20201220')
    print(dd)
    print(type(dd.Date[0]))
