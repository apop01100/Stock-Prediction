from typing import Optional, Literal
from pydantic import BaseModel
from datetime import date


class LstmTrainValidator(BaseModel):
    name: str
    symbol: str
    time_step: int
    period: Literal["1mo", "6mo", "1y"]
    train_size: float
    epochs: Optional[int] = 100
    batch_size: Optional[int] = 32
    
class LstmPredictValidator(BaseModel):
    name: str
    symbol: str