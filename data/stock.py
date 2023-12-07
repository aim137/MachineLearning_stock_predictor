import yfinance as yf
from datetime import datetime,timedelta
from pandas.core.frame import DataFrame
import pandas as pd
from sqlalchemy import create_engine

def get_stock_data(ticker: str,start_date:str = None, end_date:str = None) -> DataFrame:
    """
    Gets daily data for a stock and returns a pandas df with date and Close value.
    If either date is None, will use yfinance.download defaults
    Dates should be in the format 'YYYYMMDD', e.g., '20220202'
    """
    
    in_dates = get_dates(start_date,end_date)

    _data = update_write_db(ticker, in_dates)

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

def update_write_db(ticker,in_dates):

    engine = create_engine(f'sqlite:///daily_data_stocks.db')

    # Update or create Table in DB
    with engine.connect() as connection:

        if engine.dialect.has_table(connection,f'{ticker}'):
            db_start = pd.read_sql(f'SELECT MIN(Date) from {ticker}',engine).values[0][0]
            db_end   = pd.read_sql(f'SELECT MAX(Date) from {ticker}',engine).values[0][0]
            db_start = datetime.strptime(db_start.split(' ')[0],'%Y-%m-%d')
            db_end   = datetime.strptime(db_end.split(' ')[0],'%Y-%m-%d')

            if (in_dates[0] < db_start): 
                _data = yf.download(ticker,start = in_dates[0], end = db_start)
                _data.to_sql(f'{ticker}',engine, if_exists='append')
                print(f"Imported {len(_data)} lines")

            if (in_dates[1] > db_end): 
                _data = yf.download(ticker,start = db_end + timedelta(days=1), end = in_dates[1])
                _data.to_sql(f'{ticker}',engine, if_exists='append')
                print(f"Imported {len(_data)} lines")

        else:
            _data = yf.download(ticker,start = in_dates[0], end = in_dates[1])
            _data.to_sql(f'{ticker}',engine)
            return _data # return df if TAble in DB was created

    # Get data from DB
    _d1 = in_dates[0].strftime('%Y-%m-%d')
    _d2 = in_dates[1].strftime('%Y-%m-%d')
    _data = pd.read_sql(f"SELECT * FROM {ticker} WHERE Date BETWEEN '{_d1}' AND '{_d2}'",engine)
    return _data

if __name__ == "__main__":
    df = get_stock_data('TSLA','20201127','20201212')
    print(df)
