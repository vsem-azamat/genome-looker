FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN apt update && apt install -y libpq-dev gcc g++ zlib1g-dev libgl1-mesa-glx libglib2.0-0 bedtools

COPY backend/requirements.txt .

RUN uv pip install --system --upgrade pip && uv pip install --system -r requirements.txt
