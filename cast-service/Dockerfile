FROM python:3.8-slim

WORKDIR /app

COPY . /app/
COPY ./requirements.txt /app/requirements.txt

ENV DATABASE_URI='postgresql://cast_db_user:password@cast-service-db-service/cast_db'

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
