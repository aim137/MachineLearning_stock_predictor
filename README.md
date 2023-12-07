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

## Usage

Import run function
```python
from mlstockpredictor import driver
```
Option 1: Train model with all available data (except last 60 days) and predict tomorrow's close price based on last 60 days
```python
df, tomorrow_close = driver.run('TSLA')
```
Option 2: Build and validate a model with a given set of parameters, e.g.,
```python
my_dict = {
           'epochs': 25,
           'batch_size': 30,
           'training_days': 57,
           'is_validate': True,
          }
df, df_prediction = driver.run('TSLA', model_params=my_dict)
```
What it does:

Result of validation:
![Validation excercise for TSLA stock price](./validation/fig-TSLA-validation_up_to_20231207-00.00.00.pdf "Try it yourself!")

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This code belongs in the public domain. You are welcome to take this code and treat is as your own. 
The code is provided "as is" and must NOT be used with real money.

I am not a financial professional and this does not constitute in any way financial advice.
