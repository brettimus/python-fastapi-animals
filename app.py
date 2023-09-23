from fastapi import FastAPI, Response
import uvicorn
import asyncio
import random
import json
from autometrics import autometrics, init
from autometrics.objectives import Objective, ObjectiveLatency, ObjectivePercentile
from prometheus_client import generate_latest
from git_utils import get_git_commit, get_git_branch

app = FastAPI()

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type"
}

VERSION = "0.0.2"

init(tracker="prometheus", version=VERSION, commit=get_git_commit(), branch=get_git_branch())

# Set up a metrics endpoint for Prometheus to scrape
# `generate_latest` returns the latest metrics data in the Prometheus text format
@app.get("/metrics")
def metrics():
    return Response(generate_latest())


# Define Objectives for the api routes

API_SLO_HIGH_SUCCESS = Objective(
    "Animal API Route SLO for High Success Rate (99%)",
    success_rate=ObjectivePercentile.P99,
)

API_QUICK_RESPONSES = Objective(
    "Animal API SLO for Super Low Latency (10ms)",
    latency=(ObjectiveLatency.Ms10, ObjectivePercentile.P99),
)

ANIMALS = ["snail", "rabbit", "panda", "beaver"]


@app.get("/")
@autometrics(objective=API_SLO_HIGH_SUCCESS)
def animals():
    return {"animals": list_animals_helper()}


@app.get("/snail")
@autometrics(objective=API_QUICK_RESPONSES)
async def snail():
    # Snails are slow sometimes.
    await snail_service()
    return {"suggestion": "Let's take it easy"}


@app.route("/rabbit", methods=["GET", "OPTIONS"])
@autometrics(objective=API_QUICK_RESPONSES)
def rabbit(req):
    if req.method == "OPTIONS":
        return Response("OK", headers=CORS_HEADERS)
    # Rabbits are fast. They have very low latency
    return Response(
       json.dumps({"suggestion": "Let's drink coffee and go for a jog"}),
        headers=CORS_HEADERS
    )


@app.route("/panda", methods=["GET", "OPTIONS"])
@autometrics(objective=API_SLO_HIGH_SUCCESS)
async def panda(req):
    if req.method == "OPTIONS":
        return Response("OK", headers=CORS_HEADERS)
    # Beware! Pandas are clumsy. They error sometimes
    # await clumsy_panda_service()

    # Oh, also pandas are slow, they take their time
    # delay = random.randint(0, 11) * 0.1
    # await asyncio.sleep(delay)

    return Response(
        json.dumps({"suggestion": "Let's eat bamboo. I think I found some over th--OH NO I tripped"}),
        headers=CORS_HEADERS
    )


@app.get("/beaver")
@autometrics(objective=API_SLO_HIGH_SUCCESS)
def beaver():
    # Beavers are hard working. They never error
    return {"suggestion": "Let's build a dam"}


@autometrics
def list_animals_helper():
    """Return all animals"""
    return ANIMALS


@autometrics
async def clumsy_panda_service():
    if random.randint(1, 2) == 1:
        raise Exception("Panda service error occurred!")


@autometrics
async def snail_service():
    """Generate a random latency between 0 and 110ms"""
    delay = random.randint(0, 11) * 0.01
    await asyncio.sleep(delay)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)

