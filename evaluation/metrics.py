import numpy as np
import pandas as pd

def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
    """
    Calculate Sharpe Ratio.
    """
    excess_returns = returns - risk_free_rate
    if excess_returns.std() == 0:
        return 0
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()

def calculate_sortino_ratio(returns, risk_free_rate=0.0):
    """
    Calculate Sortino Ratio.
    """
    excess_returns = returns - risk_free_rate
    downside_returns = excess_returns[excess_returns < 0]
    if downside_returns.std() == 0:
        return 0
    return np.sqrt(252) * excess_returns.mean() / downside_returns.std()

def calculate_max_drawdown(portfolio_values):
    """
    Calculate Maximum Drawdown.
    """
    # Convert list to Series if needed
    if isinstance(portfolio_values, list):
        portfolio_values = pd.Series(portfolio_values)
        
    cum_max = portfolio_values.cummax()
    drawdown = (portfolio_values - cum_max) / cum_max
    return drawdown.min()

def calculate_var(returns, confidence_level=0.05):
    """
    Calculate Value at Risk (VaR).
    """
    return returns.quantile(confidence_level)

def calculate_cvar(returns, confidence_level=0.05):
    """
    Calculate Conditional Value at Risk (CVaR).
    """
    var = calculate_var(returns, confidence_level)
    return returns[returns <= var].mean()

def calculate_metrics(portfolio_values):
    """
    Calculate all metrics.
    """
    if isinstance(portfolio_values, list):
        portfolio_values = pd.Series(portfolio_values)
        
    returns = portfolio_values.pct_change().dropna()
    
    metrics = {
        'Total Return': (portfolio_values.iloc[-1] / portfolio_values.iloc[0]) - 1,
        'Annual Return': ((portfolio_values.iloc[-1] / portfolio_values.iloc[0]) ** (252/len(portfolio_values))) - 1,
        'Sharpe Ratio': calculate_sharpe_ratio(returns),
        'Sortino Ratio': calculate_sortino_ratio(returns),
        'Max Drawdown': calculate_max_drawdown(portfolio_values),
        'VaR (95%)': calculate_var(returns),
        'CVaR (95%)': calculate_cvar(returns)
    }
    return metrics
