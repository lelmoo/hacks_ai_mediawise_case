from fastapi import FastAPI
from get_points import get_points
from models import *

app = FastAPI()


@app.post("/evaluate")
def evaluate(eval_model: EvalModel):
    target_audience = eval_model.targetAudience
    points = eval_model.points
    return EvalModel(targetAudience=target_audience, points=points)


@app.post("/best_points")
def best_points(request: BPModel):
    target_audience = request.targetAudience
    sides = request.sides
    print(sides, target_audience)

    return get_points(request, "./points_data.csv")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
