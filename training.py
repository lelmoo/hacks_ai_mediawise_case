import pandas as pd

import geopandas as gpd
from shapely.geometry import Point

from catboost import CatBoostRegressor, Pool

import json
import pickle

import warnings

warnings.filterwarnings("ignore")


def get_direction(angle):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    direction_index = round(angle / 45) % 8
    return directions[direction_index]


def check_point_in_polygon(lat, lon, polygons):
    point = Point(lon, lat)
    for poly_name, polygon in zip(polygons["district"], polygons["geometry"]):
        if polygon.contains(point):
            return poly_name
    return None


def training(json_path, geojson_path, model_path):
    with open(json_path, "r") as file:
        json_data = json.load(file)

    data = pd.DataFrame(
        [{**json_data["targetAudience"], "points": json_data["points"]}]
    )

    gdf = gpd.read_file(geojson_path)

    for poly_name in gdf["district"]:
        data[poly_name] = 0

    for idx, row in data.iterrows():
        points = row["points"]
        for point in points:
            lat, lon, azimut = point["lat"], point["lon"], point["azimuth"]
            poly_name = check_point_in_polygon(lat, lon, gdf)
            if poly_name:
                data.at[idx, poly_name] += 1
                data["dir"] = get_direction(azimut)

    data.drop(["points", "name"], axis=1, inplace=True)

    loaded_model = pickle.load(open(model_path, "rb"))
    pred = loaded_model.predict(data)[0]
    print(pred)
    if pred < 0:
        return 0
    return pred


training("./mock_points.json", "./moscow.geojson", "./coords_model.cb")
