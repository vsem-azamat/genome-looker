FROM python:3.12-slim

RUN apt update && apt install -y libpq-dev gcc g++ zlib1g-dev libgl1-mesa-glx libglib2.0-0 bedtools

COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt