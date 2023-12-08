from mlstockpredictor import Predictor

l = ['TSLA', 'AAPL', 'GOOG', 'META', 'MSFT', 'AMZN',]
for _symbol in l:
    my_predictor = Predictor(_symbol, model_params={})
    my_predictor.run()
