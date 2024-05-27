FROM python:3.10.14-alpine3.20

WORKDIR /app

COPY ./requirments.txt .
RUN ["pip", "install","-r","requirments.txt"]
COPY tests.py .

ENTRYPOINT [ "python","tests.py"]
CMD [ "localhost:5000" ]
