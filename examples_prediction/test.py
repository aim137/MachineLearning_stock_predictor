from mlstockpredictor.driver import run

l = ['TSLA', 'AAPL', 'GOOG', 'META', 'MSFT', 'AMZN',]
l = ['AAPL']
for _symbol in l:
    run(_symbol, model_params={})
