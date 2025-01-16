from app.utils.functions.str_to_date import str_to_date
from app.utils.functions.sequences import sequences
from sklearn.preprocessing import MinMaxScaler
from app.utils.functions.check_models import check_models
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import pandas as pd
import yfinance as yf
import os

def training_new_model(params):
    try:
        stock = yf.Ticker(params["symbol"]+".JK")
        
        if stock is None:
            return {"message": "Stock not found",
                    "status": "error"}
        
        is_exist = check_models(params["name"])
        if is_exist is not None:
            return is_exist
        
        columns = ["Open", "High", "Low", "Close", "Volume"]
        data = stock.history(period=params["period"], interval="1d")
        data = data.dropna()
        data = data[columns]
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data)
        
        X, y = sequences(scaled_data, time_step=params["time_step"])
        
        train_size = int(len(X) * params["train_size"])
        X_train, X_val = X[:train_size], X[train_size:]
        y_train, y_val = y[:train_size], y[train_size:]
        
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X.shape[2])
        X_val = X_val.reshape(X_val.shape[0], X_val.shape[1], X.shape[2])
        
        model = Sequential([
            LSTM(128, input_shape=(X_train.shape[1], X_train.shape[2]),
                return_sequences=True),
            LSTM(64, return_sequences=False),
            Dense(32, activation="relu"),
            Dropout(0.2),
            Dense(5)
        ])
        
        model.compile(optimizer="adam", 
                      loss="mean_squared_error", 
                      metrics=["mae"])

        history = model.fit(X_train, y_train, 
                  epochs=params["epochs"], 
                  batch_size=params["batch_size"], 
                  validation_data=(X_val, y_val))
        
        model.save(f'../RestAPI/app/assets/ML/{params["name"]}_lstm_model.keras')
        
        # Access validation metrics from the history object
        val_mae = history.history['mae']
        val_loss = history.history['val_loss']
        
        return {"message": "Model trained successfully",
                "mae": val_mae[-1],
                "loss": val_loss[-1],
                "status": "success"
                }
    except Exception as e:
        print(f"Error training model: {e}")
        return None
        