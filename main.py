from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_methods=["*"],
    allow_headers=["*"],
)

class ForexData(BaseModel):
    data: str
    current_time: str

@app.post("/htf_data/")
def htf_data(data: ForexData):
    print(data)
    print(type(data))
    return {"message": "Data received"}

@app.post("/mtf_data/")
def htf_data(data: ForexData):
    print(data)
    print(type(data))
    return {"message": "Data received"}

@app.post("/htf_data/")
def htf_data(data: ForexData):
    print(data)
    print(type(data))
    return {"message": "Data received"}

@app.post("/trade_decision")
def htf_data(data: ForexData):
    print(data)
    print(type(data))
    return {"message": "Data received", "trade_decision": "Buy"}
