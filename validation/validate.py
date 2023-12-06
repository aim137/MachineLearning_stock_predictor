from mlstockpredictor.driver import run

l = ['TSLA', 'AAPL', 'GOOG', 'META', 'MSFT', 'AMZN', 'FVRR', 'PLTR', 'LCID']
for _symbol in l:
    run(_symbol,model_params={'is_validate':True,'epochs':4})
