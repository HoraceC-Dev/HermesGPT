from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd
from app.mtf_agent_helper import mtf_agent_operation, mtf_info_summary
from app.htf_agent_helper import htf_agent_operation
from app.trading_agent_helper import trade_decision_operation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_methods=["*"],
    allow_headers=["*"],
)

class CandleData(BaseModel):
    time: str
    open: float
    high: float
    low: float
    close: float

@app.post("/htf_data/")
def htf_data(data: List[CandleData]):
    data_dicts = [candle.model_dump() for candle in data]
    # Convert list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(data_dicts)

    htf_info = htf_agent_operation(df)
    with open("htf_info.txt", "w") as f:
        f.write(htf_info)
    return {"message": "Data received"}

@app.post("/mtf_data/")
def htf_data(data: List[CandleData]):
    data_dicts = [candle.model_dump() for candle in data]
    # Convert list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(data_dicts)

    mtf_info_1 = mtf_agent_operation(df[:100]) 
    mtf_info_2 = mtf_agent_operation(df[100:200])
    mtf_info_3 = mtf_agent_operation(df[200:300])
    mtf_info_pre_processing = mtf_info_1 + mtf_info_2 +mtf_info_3
    mtf_info_processed = mtf_info_summary(mtf_info_pre_processing)
    with open("mtf_info.txt", "w") as f:
        f.write(mtf_info_processed)
    return {"message": "Data received"}

@app.post("/trade_decision/")
def htf_data(data: List[CandleData]):
    data_dicts = [candle.model_dump() for candle in data]
    # Convert list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(data_dicts)
    htf_info = None
    mtf_info = None
    with open("mtf_info.txt", "r") as f:
        mtf_info = f.read()
    with open("htf_info.txt", "r") as f:
        htf_info = f.read()

    if htf_info==None or mtf_info==None:
        return {"trade": False}
    else:
        trading_operation_and_detail = trade_decision_operation(htf_info, mtf_info , df)

        trade_details = trading_operation_and_detail.model_dump()
    print(trade_details)

    # Example: If the last candle's close price is above 1.1300, suggest a "buy"
    if trade_details["enter_market"]:
        trade_details = {
            "trade": trade_details["enter_market"],
            "direction": "buy" if trade_details["trade_type"] == "long" else "sell",
            "volume": 0.1,
            "sl": trade_details["stop_loss"],
            "tp": trade_details["take_profit"]
        }
    else:
        trade_details = {"trade": False}
    
    return trade_details
