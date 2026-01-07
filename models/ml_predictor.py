import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, classification_report
import joblib

class MLPredictor:
    def __init__(self, model_type='rf', **kwargs):
        self.model_type = model_type
        self.model = None
        self.kwargs = kwargs
        
        if model_type == 'rf':
            self.model = RandomForestClassifier(**kwargs)
        elif model_type == 'xgb':
            self.model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', **kwargs)
        else:
            raise ValueError("Invalid model_type. Choose 'rf' or 'xgb'.")

    def prepare_data(self, df, feature_cols, target_col='Target', shift=-1):
        """
        Prepare data for ML: create target by shifting returns.
        Target: 1 if next return > 0, else 0.
        """
        data = df.copy()
        # Create target: Predict direction of next period return
        # shift(-1) means we align current features with next period's return
        data['Next_Return'] = data['Log_Return'].shift(shift)
        data[target_col] = (data['Next_Return'] > 0).astype(int)
        
        data = data.dropna()
        X = data[feature_cols]
        y = data[target_col]
        return X, y

    def train(self, X_train, y_train):
        """
        Train the model.
        """
        print(f"Training {self.model_type} model...")
        self.model.fit(X_train, y_train)
        print("Training complete.")

    def evaluate(self, X_test, y_test):
        """
        Evaluate the model.
        """
        if self.model is None:
            raise ValueError("Model not trained.")
        
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc:.4f}")
        print(classification_report(y_test, y_pred))
        return acc

    def predict(self, X):
        """
        Predict class labels.
        """
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Predict class probabilities.
        """
        return self.model.predict_proba(X)

    def save(self, path):
        joblib.dump(self.model, path)
        print(f"Model saved to {path}")

    def load(self, path):
        self.model = joblib.load(path)
        print(f"Model loaded from {path}")
