FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app/app /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --requirement requirements.txt