from pydantic import BaseModel
from typing import List

class TargetAudience(BaseModel):
    name: str
    gender: str
    ageFrom: int
    ageTo: int
    income: str


class Point(BaseModel):
    lat: str
    lon: str
    azimuth: int


class EvalModel(BaseModel):
    targetAudience: TargetAudience
    points: List[Point]


class BPModel(BaseModel):
    sides: int
    targetAudience: TargetAudience
