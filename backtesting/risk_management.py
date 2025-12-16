import numpy as np

class RiskManagement:
    def __init__(self, max_drawdown_limit=0.2, stop_loss_pct=0.05):
        self.max_drawdown_limit = max_drawdown_limit
        self.stop_loss_pct = stop_loss_pct
        
    def check_risk(self, portfolio_value, peak_value):
        drawdown = (peak_value - portfolio_value) / peak_value
        if drawdown > self.max_drawdown_limit:
            return False # Stop trading
        return True
        
    def calculate_position_size(self, capital, price, risk_per_trade=0.02):
        """
        Calculate position size based on risk per trade.
        """
        # Simple fixed fractional
        amount_to_risk = capital * risk_per_trade
        # Assuming stop loss is hit
        loss_per_share = price * self.stop_loss_pct
        shares = amount_to_risk / loss_per_share
        return int(shares)
