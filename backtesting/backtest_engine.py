import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class BacktestEngine:
    def __init__(self, initial_capital=10000.0, commission=0.001, slippage=0.001):
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.portfolio_value = []
        self.positions = []
        self.cash = []
        
    def run(self, df, signals):
        capital = self.initial_capital
        position = 0
        
        self.portfolio_value = []
        self.positions = []
        self.cash = []
        
        signals = signals.reindex(df.index).fillna(0)
        
        for i in range(len(df)):
            price = df['Close'].iloc[i]
            signal = signals.iloc[i]
            date = df.index[i]
            
            current_val = capital + (position * price)
            self.portfolio_value.append(current_val)
            self.positions.append(position)
            self.cash.append(capital)
            
            if signal == 1 and position <= 0:
                if position < 0:
                    cost = abs(position) * price
                    capital -= (cost * self.commission)
                    capital += (abs(position) * price)
                    position = 0
                
                effective_price = price * (1 + self.slippage)
                shares = int(capital / (effective_price * (1 + self.commission)))
                
                if shares > 0:
                    cost = shares * effective_price
                    capital -= cost
                    capital -= (cost * self.commission)
                    position = shares
                    
            elif signal == -1 and position >= 0:
                if position > 0:
                    revenue = position * price * (1 - self.slippage)
                    capital += revenue
                    capital -= (revenue * self.commission)
                    position = 0
                
                effective_price = price * (1 - self.slippage)
                shares = int(capital / (effective_price * (1 + self.commission)))
                
                if shares > 0:
                    revenue = shares * effective_price
                    capital += revenue
                    capital -= (revenue * self.commission)
                    position = -shares
                    
            elif signal == 0 and position != 0:
                if position > 0:
                    revenue = position * price * (1 - self.slippage)
                    capital += revenue
                    capital -= (revenue * self.commission)
                else:
                    cost = abs(position) * price * (1 + self.slippage)
                    capital -= cost
                    capital -= (cost * self.commission)
                position = 0
                
        results = pd.DataFrame({
            'Portfolio Value': self.portfolio_value,
            'Position': self.positions,
            'Cash': self.cash
        }, index=df.index)
        
        return results

    def plot_results(self, results):
        plt.figure(figsize=(12, 6))
        plt.plot(results['Portfolio Value'], label='Portfolio Value')
        plt.title('Backtest Results')
        plt.legend()
        plt.show()
