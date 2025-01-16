import numpy as np

def sequences(data, time_step=60):
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step)])
        y.append(data[i + time_step, :])
        
    X = np.array(X)
    y = np.array(y)

        
    return X, y