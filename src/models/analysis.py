"""
Data models for token analysis
"""
from dataclasses import dataclass
from typing import Literal

@dataclass
class TokenAnalysis:
    """Results from Claude's token analysis"""
    
    risk_level: int  # 1-10
    opportunity_score: int  # 1-10
    action: Literal["BUY", "SELL", "HOLD"]
    position_size_sol: float
    stop_loss_percent: float
    take_profit_percent: float
    reasoning: str
    
    @property
    def should_trade(self) -> bool:
        """Whether the analysis recommends trading"""
        return self.action in ["BUY", "SELL"]
