# Machine Learning stock price predictor

This is a python module to predic stock prices using machine learning. However, all of it is under development and must NOT, as of now, be used with real money.
 
## Installation


```bash
pip install tensorflow
pip install scikit-learn
pip install yfinance
pip install pandas
pip install numpy
clone repo
cd to repo
pip install -e .
```

## How it works

![Workflow](https://github.com/aim137/MachineLearning_stock_predictor/assets/70944449/36906510-aae3-4c6b-ac25-131d1033933c)

## Usage

Import class
```python
from mlstockpredictor import Predictor
```

Option 1: Build and validate a model with a given set of parameters, e.g.,
```python
my_dict = {
           'epochs': 25,
           'batch_size': 30,
           'training_days': 57,
           'is_validate': True,
          }
my_predictor = Predictor('TSLA', model_params=my_dict)
df, df_prediction = my_predictor.run()
```

![fig-TSLA_validation](https://github.com/aim137/MachineLearning_stock_predictor/assets/70944449/a63ec254-a4cd-4f5d-86e4-1e0e6706c46e)

Option 2: Train model with all available data (except last 60 days) and predict tomorrow's close price based on last 60 days
```python
my_dict['is_validate'] = False
another_predictor = Predictor('TSLA', model_params=my_dict)
df, tomorrow_close = another_predictor.run()
```

![fig-TSLA_prediction](https://github.com/aim137/MachineLearning_stock_predictor/assets/70944449/949d7efa-1dce-4c12-9e70-df50a7f92724)

## Unit tests

```bash
cd unit_test
```
The database `daily_data_stocks.db` can be kept or deleted.
It will be regenerated provided data can be pulled from `yfinance`.
```bash
pytest
```
All 6 tests should pass within 45 seconds.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update unit tests and examples as appropriate.

## License

This code belongs in the public domain. You are welcome to take this code and treat is as your own. 
The code is provided "as is" and must NOT be used with real money.

I am not a financial professional and this does not constitute in any way financial advice.
