import pandas as pd
import numpy as np

def calculate_rolling_stats(series, window=20):
    
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    rolling_skew = series.rolling(window=window).skew()
    rolling_kurt = series.rolling(window=window).kurt()
    
    return rolling_mean, rolling_std, rolling_skew, rolling_kurt

def calculate_autocorrelation(series, window=20, lag=1):
   
    return series.rolling(window=window).apply(lambda x: x.autocorr(lag=lag), raw=False)

def add_statistical_features(df, target_col='Log_Return', window=20):
    
    if target_col not in df.columns:
        print(f"Warning: {target_col} not in DataFrame. Skipping statistical features.")
        return df
        
    mean, std, skew, kurt = calculate_rolling_stats(df[target_col], window)
    
    df[f'{target_col}_Mean_{window}'] = mean
    df[f'{target_col}_Std_{window}'] = std
    df[f'{target_col}_Skew_{window}'] = skew
    df[f'{target_col}_Kurt_{window}'] = kurt
    
    df[f'{target_col}_Autocorr_{window}'] = calculate_autocorrelation(df[target_col], window)
    
    return df
