FROM python:3

RUN mkdir -p /code

WORKDIR /code

COPY app.py /code/app.py
COPY config.ini /code/config.ini
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

CMD [ "python", "app.py" ]