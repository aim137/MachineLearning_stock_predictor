from mlstockpredictor.mlmodel.lstm import build_model
from mlstockpredictor.data.stock import get_stock_data
df = get_stock_data('TSLA')
t,v = build_model(df,validation = True)
