from mlstockpredictor.mlmodel.lstm import build_model,validate_model,predict_tomorrow
from mlstockpredictor.data.stock import get_stock_data
from mlstockpredictor.aux.functions import plot_prediction
from mlstockpredictor.aux.defaults import default_model_params
from collections import ChainMap


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Run prediction one time to get tomorrow's estimated Close price
# or validate a model with a given set of parameters
# <><><><><>
#def run(ticker: str, training_days: int = 60 , split_frac: float = 0.8 , plot: bool = True , model_params['is_validate']: bool = False) -> tuple:
def run(ticker: str, start: str = None, end: str = None, model_params: dict = {}) -> tuple:

  model_params = dict(ChainMap(model_params,default_model_params))

  df = get_stock_data(ticker,start_date=start,end_date=end)
  
  if model_params['is_validate'] and (df.shape[0] - int(df.shape[0]*model_params['split_frac']) <= model_params['training_days']):
    raise ValueError("The number of datapoints requested for each prediction exceedes the size of the dataframe provided")

  if model_params['is_validate']:
    # Use {split_frac*100}% of the data to train the model 
    # and the las {(1-split_frac)*100}% to test it
    train_df = df.iloc[ : int(df.shape[0]*model_params['split_frac']), : ]
    test_df  = df.iloc[int(df.shape[0]*model_params['split_frac']) : , : ]
  else:
    # Use the last {training_days} days to predict the close close tomorrow
    # Use the remaining (earlier) data to train the model
    train_df = df.iloc[ : -model_params['training_days'], : ]
    test_df  = df.iloc[-model_params['training_days'] : , : ]
  
  # Build model
  model = build_model(train_df,model_params)
  
  if model_params['is_validate']:
    prediction = validate_model(model,test_df,model_params)
  else:
    prediction = predict_tomorrow(model,test_df)

  if plot:
    plot_prediction(df,prediction,ticker=ticker,is_validate=model_params['is_validate'])

  return test_df, prediction
  
  
if __name__ == "__main__":
  _test_df, close_tomorrow = run('TSLA')
