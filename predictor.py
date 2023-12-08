from mlstockpredictor.mlmodel.lstm import build_model,validate_model,predict_tomorrow
from mlstockpredictor.data.stock import get_stock_data
from mlstockpredictor.aux.functions import plot_prediction
from mlstockpredictor.aux.defaults import default_model_params
from collections import ChainMap


# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Run prediction one time to get tomorrow's estimated Close price
# or validate a model with a given set of parameters
# <><><><><>
class Predictor():

  def __init__(self,ticker: str, start: str = None, end: str = None, model_params: dict = {}):
  
    self.ticker = ticker
    self.start  = start
    self.end    = end
    self.model_params = dict(ChainMap(model_params,default_model_params))
    # Expose some keys
    self.is_validate = self.model_params['is_validate']
    self.should_plot = self.model_params['should_plot']
    self.should_report = self.model_params['should_report']
  
    self.df = get_stock_data(ticker,start_date=start,end_date=end)
    
    if self.is_validate:
      if (self.df.shape[0] - int(self.df.shape[0]*self.model_params['split_frac']) <= self.model_params['training_days']):
        raise ValueError("The number of datapoints requested for each prediction exceedes the size of the dataframe provided")
  
    if self.is_validate:
      # Use {split_frac*100}% of the data to train the model 
      # and the las {(1-split_frac)*100}% to test it
      self.train_df = self.df.iloc[ : int(self.df.shape[0]*self.model_params['split_frac']), : ]
      self.test_df  = self.df.iloc[int(self.df.shape[0]*self.model_params['split_frac']) : , : ]
    else:
      # Use the last {training_days} days to predict the close close tomorrow
      # Use the remaining (earlier) data to train the model
      self.train_df = self.df.iloc[ : -self.model_params['training_days'], : ]
      self.test_df  = self.df.iloc[-self.model_params['training_days'] : , : ]
    
    # Build model
    self.model = build_model(self.train_df,self.model_params)

  def run(self):
    
    if self.is_validate:
      self.prediction = validate_model(self.model,self.test_df,self.model_params['training_days'])
    else:
      self.prediction = predict_tomorrow(self.model,self.test_df)
  
    if self.should_plot:
      plot_prediction(self.df,self.prediction,ticker=self.ticker,is_validate=self.is_validate)

    if self.should_report:
      self.report()
  
    return self.test_df, self.prediction

  def report(self):
    pass

  
  
if __name__ == "__main__":
  predictor = Predictor('TSLA')
  _test_df, close_tomorrow = Predictor.run()
