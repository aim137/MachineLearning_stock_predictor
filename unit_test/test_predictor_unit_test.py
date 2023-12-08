import pytest
from datetime import date
from mlstockpredictor import Predictor
from unittest.mock import Mock

@pytest.fixture
def quicktest_params():
    quicktest_params = {
    'split_frac'     : 0.8,
    'training_days'  : 30,
    'lstm_units_1'   : 20,
    'lstm_units_2'   : 20,
    'lstm_units_3'   : 20,
    'epochs'         : 3,
    'batch_size'     : 12,
    'is_validate'    : False,
    'should_plot'    : False,
    'should_report'  : False,
                        }
    
    return 'TSLA','2022-03-12','2023-11-25',quicktest_params


def test_identify_weekdays(quicktest_params):
    p_1 = Predictor(*quicktest_params)
    assert p_1.start == date(2022,3,14)
    assert p_1.end   == date(2023,11,24)

def test_prediction_case(quicktest_params):
    p_1 = Predictor(*quicktest_params)
    _df, prediction = p_1.run()
    assert prediction[0][0] >= 0.98*float(223.79968)
    assert prediction[0][0] <= 1.02*float(223.79968)

def test_validation_case(quicktest_params):
    quicktest_params[3]['is_validate'] = True
    p_1 = Predictor(*quicktest_params)
    _df, validation = p_1.run()
    assert validation[-1][0] >= 0.98*float(223.77795)
    assert validation[-1][0] <= 1.02*float(223.77795)

def test_enough_days_prediction(quicktest_params):
    quicktest_params[3]['training_days'] = 429
    with pytest.raises(ValueError):
        p_1 = Predictor(*quicktest_params)

def test_enough_days_validation(quicktest_params):
    quicktest_params[3]['training_days'] = 86
    quicktest_params[3]['is_validate'] = True
    with pytest.raises(ValueError):
        p_1 = Predictor(*quicktest_params)
