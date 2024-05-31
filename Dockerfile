FROM python:3.10.14-alpine3.20
EXPOSE 5000

WORKDIR /app
COPY ./requirments.txt .
RUN ["pip", "install","-r","requirments.txt"]

COPY ./src/*.py .


ENTRYPOINT [ "python","app.py" ]