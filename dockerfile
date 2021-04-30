FROM python:3.8

WORKDIR /code

ADD . /code

RUN pip3 install -r requirements.txt

CMD ["python","app.py"]

