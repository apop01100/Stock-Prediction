import pandas_ta as ta

def calculate_technical_indicators(data, window, std):
    data["SMA"] = ta.sma(data["Close"], length=window)
    data["EMA"] = ta.ema(data["Close"], length=window)
    data["RSI"] = ta.rsi(data["Close"], length=window)
    data = data.join(ta.bbands(data["Close"], 
                               length=window, 
                               std=std)[[f"BBL_{window}_{std}", f"BBM_{window}_{std}",f"BBU_{window}_{std}"]])
    
    data = data.dropna()
    
    return data