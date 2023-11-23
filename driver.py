from mlstockpredictor.mlmodel.lstm import build_model,predict_tomorrow
from mlstockpredictor.data.stock import get_stock_data
from mlstockpredictor.aux.functions import plot_prediction

def run(ticker,training_days,plot=True):

  df = get_stock_data(ticker)

  # Use the last {training_days} days to predict the close close tomorrow
  train_df =   df.iloc[ : -training_days, : ]
  predict_df = df.iloc[-training_days : , : ]
  
  model = build_model(train_df,validation = False)
  
  close_tomorrow = predict_tomorrow(predict_df, model)
  
  plot_prediction(df,close_tomorrow)
 
  return close_tomorrow
  
  
if __name__ == "__main__":
  close_tomorrow = run('TSLA',60)
