from catboost.core import json
from fastapi import FastAPI
from get_points import get_points
from models import *
from training import training

app = FastAPI()


@app.post("/evaluate")
def evaluate(eval_model: EvalModel):
    target_audience = eval_model.targetAudience
    points = eval_model.points
    pred = training(
        {
            "targetAudience": target_audience.model_dump(),
            "points": list(map(BaseModel.model_dump, points)),
        },
        "./moscow.geojson",
        "./coords_model.cb",
    )
    md = EvalModel(targetAudience=target_audience, points=points).model_dump_json()
    ret = json.loads(md)
    ret["value"] = pred
    return ret


@app.post("/best_points")
def best_points(request: BPModel):
    target_audience = request.targetAudience
    sides = request.sides
    print(sides, target_audience)

    return json.loads(get_points(request, "./points_data.csv"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run(app, host="127.0.0.1", port=8000)
