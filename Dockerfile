FROM python:3.11.8-alpine3.19

WORKDIR /app

COPY . .

RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev zlib-dev postgresql-dev
RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r requirements.txt
RUN apk --purge del .build-deps

CMD ["python", "main.py"]

EXPOSE 8000
