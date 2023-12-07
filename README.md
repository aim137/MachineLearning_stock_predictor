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

![Workflow](https://github.com/aim137/MachineLearning_stock_predictor/assets/70944449/00a78b4b-e835-4696-a27e-9e88418760b8)

## Usage

Import run function
```python
from mlstockpredictor import driver
```

Option 1: Build and validate a model with a given set of parameters, e.g.,
```python
my_dict = {
           'epochs': 25,
           'batch_size': 30,
           'training_days': 57,
           'is_validate': True,
          }
df, df_prediction = driver.run('TSLA', model_params=my_dict)
```

![fig-TSLA_validation](https://github.com/aim137/MachineLearning_stock_predictor/assets/70944449/a63ec254-a4cd-4f5d-86e4-1e0e6706c46e)

Option 2: Train model with all available data (except last 60 days) and predict tomorrow's close price based on last 60 days
```python
my_dict['is_validate'] = False
df, tomorrow_close = driver.run('TSLA', model_params=my_dict)
```

![fig-TSLA_prediction](https://github.com/aim137/MachineLearning_stock_predictor/assets/70944449/949d7efa-1dce-4c12-9e70-df50a7f92724)


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This code belongs in the public domain. You are welcome to take this code and treat is as your own. 
The code is provided "as is" and must NOT be used with real money.

I am not a financial professional and this does not constitute in any way financial advice.
