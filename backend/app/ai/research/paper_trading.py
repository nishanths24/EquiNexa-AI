from typing import List, Dict, Any, Optional
from datetime import datetime

class PaperPortfolio:
    def __init__(self, initial_cash: float = 100000.0, transaction_cost_pct: float = 0.001):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, dict] = {}
        self.history: List[dict] = []
        self.transaction_cost_pct = transaction_cost_pct
        
    def evaluate_signals(self, predictions: List[dict], market_prices: Dict[str, float], timestamp: datetime):
        """
        Takes live predictions and current market prices, 
        and updates the paper portfolio (entry/exit).
        """
        # Extremely simplified logic for simulation
        
        # 1. Exit logic (e.g. holding period ended)
        to_remove = []
        for ticker, pos in self.positions.items():
            # If 5 days passed
            if (timestamp - pos['entry_time']).days >= 5:
                exit_price = market_prices.get(ticker)
                if exit_price:
                    value = pos['shares'] * exit_price
                    fee = value * self.transaction_cost_pct
                    self.cash += (value - fee)
                    self.history.append({
                        "ticker": ticker,
                        "action": "SELL",
                        "price": exit_price,
                        "shares": pos['shares'],
                        "timestamp": timestamp,
                        "pnl": (exit_price - pos['entry_price']) * pos['shares'] - fee - pos['fee']
                    })
                    to_remove.append(ticker)
        
        for t in to_remove:
            del self.positions[t]
            
        # 2. Entry logic
        for p in predictions:
            ticker = p['ticker']
            prob = p['predicted_probability']
            
            if prob > 0.6 and ticker not in self.positions:
                price = market_prices.get(ticker)
                if price and self.cash > 1000:
                    # Risk 10% of cash
                    invest_amt = self.cash * 0.10
                    shares = invest_amt / price
                    fee = invest_amt * self.transaction_cost_pct
                    
                    self.cash -= (invest_amt + fee)
                    self.positions[ticker] = {
                        "shares": shares,
                        "entry_price": price,
                        "entry_time": timestamp,
                        "fee": fee
                    }
                    self.history.append({
                        "ticker": ticker,
                        "action": "BUY",
                        "price": price,
                        "shares": shares,
                        "timestamp": timestamp
                    })
                    
    def get_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        val = self.cash
        for ticker, pos in self.positions.items():
            price = current_prices.get(ticker, pos['entry_price'])
            val += pos['shares'] * price
        return val
