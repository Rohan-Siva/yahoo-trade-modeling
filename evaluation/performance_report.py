import pandas as pd
import matplotlib.pyplot as plt
from .metrics import calculate_metrics

def generate_report(results, benchmark=None):
    """
    Generate performance report.
    """
    portfolio_values = results['Portfolio Value']
    metrics = calculate_metrics(portfolio_values)
    
    print("Performance Report")
    print("==================")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")
        
    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(portfolio_values, label='Strategy')
    if benchmark is not None:
        # Normalize benchmark to start at same value
        benchmark = benchmark / benchmark.iloc[0] * portfolio_values.iloc[0]
        plt.plot(benchmark, label='Benchmark', alpha=0.7)
        
    plt.title('Portfolio Performance')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Drawdown plot
    cum_max = portfolio_values.cummax()
    drawdown = (portfolio_values - cum_max) / cum_max
    
    plt.figure(figsize=(14, 4))
    plt.plot(drawdown, color='red', alpha=0.6)
    plt.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.2)
    plt.title('Drawdown')
    plt.grid(True)
    plt.show()
