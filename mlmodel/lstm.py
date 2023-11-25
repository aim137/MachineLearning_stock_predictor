import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from matplotlib import pyplot as plt
#from icecream import ic

def build_model(train_data,training_days):
    """
    Build ML model
    """
    x_train, y_train, scaler = prepare_close_data(train_data,training_days)

    # Build model
    model = Sequential()

    model.add(LSTM(units=50, return_sequences = True, input_shape=(x_train.shape[1],1)))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50, return_sequences = True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50))
    model.add(Dropout(0.2))

    model.add(Dense(units=1))

    model.compile(optimizer = 'adam', loss = 'mean_squared_error')
    model.fit(x_train, y_train, epochs = 25, batch_size=32)
    

    #model.save('saved_model') #and then we can load it and use it
    return model


def validate_model(model,test_data,training_days):

    x_test, y_test, scaler = prepare_close_data(test_data,training_days) 
    y_validation = model.predict(x_test)
    y_validation = scaler.inverse_transform(y_validation)
    #y_test = scaler.inverse_transform(y_test.reshape(-1,1)) # y_test no longer returned

    return y_validation

def predict_tomorrow(model,latest_df):

    x_predict, y_dummy, scaler = prepare_close_data(
                                        latest_df,
                                        training_days=latest_df.shape[0],
                                        predict_days=1
                                        )

    prediction = model.predict(x_predict)

    return scaler.inverse_transform(prediction.reshape(-1,1))

def prepare_close_data(_df_in,training_days,predict_days=0):
    """
    Prepares the data for use with LSTM, returns a NumPy array.
    """
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(_df_in['Close'].values.reshape(-1,1))

    x_train, y_train = [], []

    for x in range(training_days,scaled_data.shape[0]+predict_days):
        x_train.append(scaled_data[x-training_days:x,0])
        try:
            y_train.append(scaled_data[x,0])
        except IndexError:
            pass
    
    if x is None: raise ValueError("The number of datapoints requested for each prediction exceedes the size of the dataframe provided")

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    return x_train, y_train, scaler


if __name__ == "__main__":
    from mlstockpredictor.data.stock import get_stock_data
    df = get_stock_data('TSLA')
    split_frac=0.8
    train_data = df[ : int(df.shape[0]*split_frac)]
    test_data  = df[int(df.shape[0]*split_frac) : ]
    model = build_model(train_data)
    validate_model(model,test_data,60)

    
