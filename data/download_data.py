import yfinance as yf
import pandas as pd
import os
import argparse

def download_data(tickers, start_date, end_date, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Downloading data for: {tickers}")
    data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')
    
    if len(tickers) == 1:
        ticker = tickers[0]
        file_path = os.path.join(output_dir, f"{ticker}.csv")
        data.to_csv(file_path)
        print(f"Saved {ticker} to {file_path}")
    else:
        for ticker in tickers:
            ticker_data = data[ticker]
            file_path = os.path.join(output_dir, f"{ticker}.csv")
            ticker_data.to_csv(file_path)
            print(f"Saved {ticker} to {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download financial data.')
    parser.add_argument('--tickers', nargs='+', default=['SPY', 'AAPL', 'BTC-USD'], help='List of tickers')
    parser.add_argument('--start', type=str, default='2020-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, default='2023-01-01', help='End date (YYYY-MM-DD)')
    parser.add_argument('--output', type=str, default='data/raw', help='Output directory')
    
    args = parser.parse_args()
    
    download_data(args.tickers, args.start, args.end, args.output)
