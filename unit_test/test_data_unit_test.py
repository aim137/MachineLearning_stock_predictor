import pytest
import pandas as pd
from sqlalchemy import create_engine
from datetime import date,timedelta
from mlstockpredictor import Predictor
from unittest.mock import Mock

@pytest.fixture
def overwrite_database():
    d0 = date(1998,7,8)
    l_dates = [d0+timedelta(days=n) for n in range(10) if n != 3 and n!= 4]
    l_floats = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    known_df=pd.DataFrame(
        list(zip(l_dates,l_floats,l_floats,l_floats,l_floats,l_floats,l_floats,)),
        columns=["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
                         )

    engine = create_engine('sqlite:///daily_data_stocks.db')
    known_df.to_sql('AAPL',engine,if_exists='replace')

@pytest.fixture
def quicktest_params():
    quicktest_params = {
    'split_frac'     : 0.8,
    'training_days'  : 3,
    'lstm_units_1'   : 20,
    'lstm_units_2'   : 20,
    'lstm_units_3'   : 20,
    'epochs'         : 3,
    'batch_size'     : 12,
    'is_validate'    : False,
    'should_plot'    : False,
    'should_report'  : False,
                        }
    
    return 'AAPL','1998-07-06','1998-07-21',quicktest_params


def test_n_lines_pulled(quicktest_params,overwrite_database):
    p_1 = Predictor(*quicktest_params)
    assert p_1.n_lines_pulled == 4 #correspond to missing data in DB, 6/7, 7/7, 20/7 adn 21/7
