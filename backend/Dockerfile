FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV API_BASE_URL=https://api.example.com
ENV MAX_UPLOAD_BYTES=31457280
ENV CORS_ALLOW_ORIGINS=
ENV CORS_ALLOW_ORIGIN_REGEX=^https://.*\.vercel\.app$

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
