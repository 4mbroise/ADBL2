from infer import relationsClf
from fastapi import FastAPI
from websockets.sync.client import connect
import lmql
from pydantic import BaseModel, validator
from enum import Enum
from typing import Optional
import json
from typing import Literal
from load_model import load_model_and_tokenizer
from fastapi.middleware.cors import CORSMiddleware
import requests


origins = [
    "http://192.168.237.233:27019",
    "http://192.168.237.233:10250",
    "http://192.168.237.233:10251",
    "http://192.168.237.233:10252",
    "http://192.168.237.233:10253",
    "http://localhost:27019"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

promptTechniques = ["fixed-4-shots", "0-shot"]

completion = ["attack", "support"]

model = lmql.model("google/gemma-2b", endpoint="lmql:4000")
model = None

with open("models_config.json") as json_config_file:
    modelConfigs = json.load(json_config_file)

class LlmModelEnum(Enum):
    gpt2Medium = "gpt2-medium"
    gemma_2b = "google/gemma-2b"

class PredictionQuery(BaseModel):
    model: Literal[tuple(modelConfigs)]
    topArgument : str
    subArgument : str
    promptTechnique : Literal[tuple(promptTechniques)]
    # modelPath: Optional[str] = None
    # @validator("modelPath", always=True)
    # def validate_date(cls, value, values):
    #     print(modelConfigs[values["model"]]["modelType"])
    #     print(modelConfigs[values["model"]]["modelType"] == "llamaCpp" and value is None)
    #     if modelConfigs[values["model"]]["modelType"] == "llamaCpp" and value is None:
    #         raise ValueError('Model path missing')

class PredictionResult(BaseModel):
    attack: float
    support: float
    prompt: str



@app.post("/predict")
async def predict(body: PredictionQuery) -> PredictionResult :
    model = load_model_and_tokenizer(modelConfigs[body.model])
    modelConfig = modelConfigs[body.model]
    
    res = await relationsClf(model, body.topArgument, body.subArgument, body.promptTechnique, modelConfig["promptTemplate"])
    return res

@app.get("/ping")
async def ping():
    resp = requests.get("http://ping:80/ping")
    return {
        "code" : resp.status_code,
        "test" : resp.text
    }

@app.get("/model")
async def predict():
    return model

@app.get("/models")
async def predict():
    return {"modelList" : list(modelConfigs)}

@app.get("/prompt-techniques")
async def predict():
    return {"promptTechniques" : list(promptTechniques)}
