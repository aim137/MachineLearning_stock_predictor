from mlstockpredictor.mlmodel.lstm import build_model,validate_model,predict_tomorrow
from mlstockpredictor.data.stock import get_stock_data
from mlstockpredictor.aux.functions import plot_prediction


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Run prediction one time to get tomorrow's estimated Close price
# or validate a model with a given set of parameters
# <>
def run(ticker,training_days=60,split_frac=0.8,plot=True,mode_validate=False):

  df = get_stock_data(ticker) #aim137 agregar fechas
  
  if mode_validate and (df.shape[0] - int(df.shape[0]*split_frac) <= training_days):
    raise ValueError("The number of datapoints requested for each prediction exceedes the size of the dataframe provided")

  if mode_validate:
    # Use {split_frac*100}% of the data to train the model 
    # and the las {(1-split_frac)*100}% to test it
    train_df = df.iloc[ : int(df.shape[0]*split_frac), : ]
    test_df  = df.iloc[int(df.shape[0]*split_frac) : , : ]
  else:
    # Use the last {training_days} days to predict the close close tomorrow
    # Use the remaining (earlier) data to train the model
    train_df = df.iloc[ : -training_days, : ]
    test_df  = df.iloc[-training_days : , : ]
  
  # Build model
  model = build_model(train_df,training_days)
  
  if mode_validate:
    prediction = validate_model(model,test_df,training_days)
  else:
    prediction = predict_tomorrow(model,test_df)

  if plot:
    plot_prediction(df,prediction,ticker=ticker,mode_validate=mode_validate)

  return test_df, prediction
  
  
if __name__ == "__main__":
  _test_df, close_tomorrow = run('TSLA')
