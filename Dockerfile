FROM python:3.7-alpine

WORKDIR /app

# Install Dependencies
COPY requirements.txt ./
RUN apk add --no-cache --virtual .build-deps \
    build-base && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

ENV FLASK_APP=run.py
COPY . .

CMD [ "python", "./run.py" ]
