import pandas as pd
import numpy as np

class MLStrategy:
    def __init__(self, model, feature_cols):
        self.model = model
        self.feature_cols = feature_cols

    def generate_signals(self, df):
        """
        Generate trading signals based on ML predictions.
        Signal: 1 (Long) if predicted up, -1 (Short) if predicted down (or 0 if flat).
        """
        # Ensure features exist
        missing_cols = [c for c in self.feature_cols if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing feature columns: {missing_cols}")
            
        X = df[self.feature_cols]
        
        # Predict
        # Assuming binary classification: 1 = Up, 0 = Down
        predictions = self.model.predict(X)
        
        # Convert 0 to -1 for Short signal, or keep 0 for cash?
        # Let's say 0 -> -1 (Short) for a long/short strategy
        signals = np.where(predictions == 1, 1, -1)
        
        return pd.Series(signals, index=df.index)
