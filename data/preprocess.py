import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
import os
import argparse

def load_data(file_path):
    return pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

def calculate_returns(df, price_col='Close'):

    df['Log_Return'] = np.log(df[price_col] / df[price_col].shift(1))
    return df.dropna()

def check_stationarity(series):

    result = adfuller(series)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))
    
    if result[1] < 0.05:
        print("Series is stationary")
        return True
    else:
        print("Series is non-stationary")
        return False

def preprocess(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".csv") and "_processed" not in file_name:
            print(f"Processing {file_name}...")
            file_path = os.path.join(input_dir, file_name)
            df = load_data(file_path)
            
           
            price_col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
            
            df = calculate_returns(df, price_col)
            
            print(f"Stationarity test for {file_name} (Log Returns):")
            check_stationarity(df['Log_Return'])
            
            output_path = os.path.join(output_dir, file_name.replace(".csv", "_processed.csv"))
            df.to_csv(output_path)
            print(f"Saved processed data to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='data/raw', help='Input directory')
    parser.add_argument('--output', type=str, default='data/processed', help='Output directory')
    args = parser.parse_args()
    
    preprocess(args.input, args.output)
