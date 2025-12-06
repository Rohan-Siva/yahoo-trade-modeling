import pandas as pd
import numpy as np
from arch import arch_model
import matplotlib.pyplot as plt
import joblib

class GarchModel:
    def __init__(self, p=1, q=1, mean='Zero', vol='GARCH', dist='Normal'):
        self.p = p
        self.q = q
        self.mean = mean
        self.vol = vol
        self.dist = dist
        self.model = None
        self.fit_model = None

    def fit(self, returns):
        print(f"Fitting {self.vol}({self.p}, {self.q}) model...")
        # scale returns to avoid convergence issues if they are too small
        scaled_returns = returns * 100
        
        self.model = arch_model(scaled_returns, p=self.p, q=self.q, mean=self.mean, vol=self.vol, dist=self.dist)
        self.fit_model = self.model.fit(disp='off')
        print(self.fit_model.summary())
        return self.fit_model

    def predict(self, horizon=5):
        if self.fit_model is None:
            raise ValueError("Model not fitted yet.")
        
        forecasts = self.fit_model.forecast(horizon=horizon)
        # return variance forecast
        return forecasts.variance.iloc[-1]

    def save(self, path):
        joblib.dump(self.fit_model, path)
        print(f"Model saved to {path}")

if __name__ == "__main__":
    # example usage
    returns = pd.Series(np.random.randn(1000))
    
    garch = GarchModel(p=1, q=1)
    garch.fit(returns)
    pred_var = garch.predict(horizon=5)
    print("Predicted Variance:", pred_var)
