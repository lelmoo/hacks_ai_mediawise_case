FROM python:3.12
WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./*.py .
COPY ./coords_model.cb .
COPY ./moscow.geojson .
COPY ./points_data.csv .

EXPOSE 8000
CMD ["python", "main.py"]
