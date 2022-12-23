FROM python:3.11-alpine3.16

COPY requirements.txt ./

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev
RUN pip install mysqlclient  
RUN apk del build-deps

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

RUN chmod +x gunicorn.sh

CMD ["gunicorn" , "--bind", "0.0.0.0:5000", "app:app"]
#ENTRYPOINT [ "./gunicorn.sh" ]

#CMD ["python3", "./app.py"]