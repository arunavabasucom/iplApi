import os
import json
import uvicorn
import sentry_sdk
import pandas as pd
from typing import Optional
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware 

load_dotenv() 

sentry_sdk.init(
  dsn=os.environ['SENTRY_DSN'],
    environment=os.environ['SENTRY_ENVIRONMENT'],
    traces_sample_rate=1.0,
    )



app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

@app.get("/")
async def root():
    return {"message": "Hello World"} 

@app.get("/match")
async def match_data(team:Optional[str] = None,city:Optional[str] = None,winner:Optional[str] = None):
    df = pd.read_csv("data/IPL Matches 2008-2020.csv")
    json_data = df.to_json(orient="records")
    if team:
        rows_with_team = df[(df['team1'] == team) | (df['team2'] == team)]
        json_data = rows_with_team.to_json(orient="records")
    if city:
        rows_with_city = df[df['city'] == city]
        json_data = rows_with_city.to_json(orient="records")
    if winner:
        rows_with_winner = df[df['winner'] == winner]
        json_data = rows_with_winner.to_json(orient="records")
    if team and city :
        rows_with_team_city = df[((df['team1'] == team) | (df['team2'] == team)) &(df['city'] == city) ]
        json_data = rows_with_team_city.to_json(orient="records")
    if city and winner : 
        rows_with_city_winner = df[(df['city'] == city) &(df['winner'] == winner) ]
        json_data = rows_with_city_winner.to_json(orient="records")
    if team and winner :
        rows_with_team_winner = df[((df['team1'] == team) | (df['team2'] == team)) &(df['winner'] == winner) ]
        json_data = rows_with_team_winner.to_json(orient="records")
    if team and city and winner:
        rows_with_team_city_winner = df[(df['winner'] == winner) &(df['city'] == city) &((df['team1'] == team) | (df['team2'] == team)) ]
        json_data = rows_with_team_city_winner.to_json(orient="records")     
    data = json.loads(json_data) 
    return data

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)