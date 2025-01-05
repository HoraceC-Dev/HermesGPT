from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_methods=["*"],
    allow_headers=["*"],
)

class CandleData(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float

@app.post("/htf_data/")
def htf_data(data: List[CandleData]):
    print(data)
    print(type(data))
    return {"message": "Data received"}

@app.post("/mtf_data/")
def htf_data(data: List[CandleData]):
    print(data)
    print(type(data))
    return {"message": "Data received"}

@app.post("/htf_data/")
def htf_data(data: List[CandleData]):
    print(data)
    print(type(data))
    return {"message": "Data received"}

@app.post("/trade_decision")
def htf_data(data: List[CandleData]):
    
    # Example: If the last candle's close price is above 1.1300, suggest a "buy"
    if data[-1].close > 1.1300:
        trade_decision = True
        trade_details = {
            "trade": True,
            "direction": "buy",
            "volume": 0.1,
            "sl": 1.1280,
            "tp": 1.1350
        }
    else:
        trade_details = {"trade": False}

    return trade_details
