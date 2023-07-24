#не могу сделать entrypoint.sh. Как не потылся, перепровбовал 50 вараинтов и комбинаций.
# каждый раз контейнер либо бесконечно starting... , либо старутет и перезагружается.

FROM python:3.9-slim

WORKDIR /app

RUN pip install gunicorn==20.1.0

RUN pip install python-dotenv

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
