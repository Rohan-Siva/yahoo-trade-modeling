import pandas as pd
import numpy as np
import pmdarima as pm
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import joblib
import os

class ArimaModel:
    def __init__(self, order=None, seasonal=False):
        self.order = order
        self.seasonal = seasonal
        self.model = None
        self.fit_model = None

    def auto_fit(self, series, seasonal_m=1):
        """
        Auto-fit ARIMA model using pmdarima.
        """
        print("Auto-fitting ARIMA model...")
        self.model = pm.auto_arima(series, 
                                   seasonal=self.seasonal, 
                                   m=seasonal_m,
                                   suppress_warnings=True, 
                                   stepwise=True,
                                   trace=True)
        self.fit_model = self.model
        print(f"Best model: {self.model.order}")
        return self.model.summary()

    def fit(self, series, order=None):

        if order is None:
            order = self.order
            
        print(f"Fitting ARIMA model with order {order}...")
        self.model = ARIMA(series, order=order)
        self.fit_model = self.model.fit()
        print(self.fit_model.summary())
        return self.fit_model

    def predict(self, n_periods=10):

        if self.fit_model is None:
            raise ValueError("Model not fitted yet.")
        
        if hasattr(self.fit_model, 'predict'):
             return self.fit_model.forecast(steps=n_periods)
        else:
            return self.fit_model.predict(n_periods=n_periods)

    def save(self, path):
        joblib.dump(self.fit_model, path)
        print(f"Model saved to {path}")

    def load(self, path):
        self.fit_model = joblib.load(path)
        print(f"Model loaded from {path}")

if __name__ == "__main__":
    data = np.random.randn(100).cumsum()
    series = pd.Series(data)
    
    arima = ArimaModel()
    arima.auto_fit(series)
    forecast = arima.predict(n_periods=5)
    print("Forecast:", forecast)
