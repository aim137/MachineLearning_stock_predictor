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

```python
from mlstockpredictor import driver

driver.run('TSLA',60) # Predict tomorrow's close price based on last 60 days

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This code belongs in the public domain. You are welcome to take this code and treat is as your own. 
The code is provided "as is" and must NOT be used with real money.

I am not a financial professional and this does not constitute in any way financial advice.
