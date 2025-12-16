class Portfolio:
    def __init__(self, initial_capital=10000.0):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = {} # Symbol -> Quantity
        self.holdings_value = 0.0
        
    def update_position(self, symbol, quantity, price):
        if symbol not in self.positions:
            self.positions[symbol] = 0
        self.positions[symbol] += quantity
        
    def get_value(self, current_prices):
        val = self.current_capital
        for symbol, qty in self.positions.items():
            if symbol in current_prices:
                val += qty * current_prices[symbol]
        return val
