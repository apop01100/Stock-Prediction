from app.utils.functions.check_models import check_models
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import yfinance as yf

def predict_stock_price(params):
    is_exist = check_models(params['name'])
    if is_exist is not None:
        model = load_model(f"app//assets/ML/{params['name']}_lstm_model.keras")
    else:
        model = load_model("app/assets/ML/lstm_model.keras")
    
    stock = yf.Ticker(params['symbol']+".JK")
    data = stock.history(period="1d", interval="1d")
    data = data.dropna()
    data = data[["Open", "High", "Low", "Close", "Volume"]]
    
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    scaled_data = scaled_data.reshape(1, scaled_data.shape[0], scaled_data.shape[1])
    
    prediction = model.predict(scaled_data)
    prediction = scaler.inverse_transform(prediction)
    
    next_day = data.index[-1] + timedelta(days=1)
    next_day_str = next_day.strftime("%Y-%m-%d")
    
    return {    
                "date": next_day_str,
                "prediction": {
                    "Open": f"{prediction[0][0]:.2f}",
                    "High": f"{prediction[0][1]:.2f}",
                    "Low": f"{prediction[0][2]:.2f}",
                    "Close": f"{prediction[0][3]:.2f}"
                    },
                "status": "success"
            }