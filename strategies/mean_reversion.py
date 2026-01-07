import pandas as pd
import numpy as np

class MeanReversionStrategy:
    def __init__(self, window=20, num_std=2):
        self.window = window
        self.num_std = num_std

    def generate_signals(self, df):
        """
        Generate signals based on Bollinger Bands.
        Long if price < Lower Band
        Short if price > Upper Band
        Exit if price crosses Mean? Or just hold until opposite signal?
        Let's do:
        - Long (1) if Close < Lower Band
        - Short (-1) if Close > Upper Band
        - Neutral (0) otherwise (or hold previous)
        """
        # Calculate bands if not present
        if 'BB_Upper' not in df.columns or 'BB_Lower' not in df.columns:
            rolling_mean = df['Close'].rolling(window=self.window).mean()
            rolling_std = df['Close'].rolling(window=self.window).std()
            upper_band = rolling_mean + (rolling_std * self.num_std)
            lower_band = rolling_mean - (rolling_std * self.num_std)
        else:
            upper_band = df['BB_Upper']
            lower_band = df['BB_Lower']
            
        signals = pd.Series(0, index=df.index)
        
        # Vectorized signal generation
        signals[df['Close'] < lower_band] = 1
        signals[df['Close'] > upper_band] = -1
        
        # Fill zeros with previous signal to hold position? 
        # Or is this a mean reversion where we exit at mean?
        # Let's implement: Enter at band, Exit at mean.
        # This is harder to vectorize purely without loop if we have state (in position or not).
        # For simplicity in vector backtest, let's just return the raw signals and let backtester handle logic,
        # OR return a series of target positions.
        
        return signals
