FROM python:slim
WORKDIR /root

COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./ ./

CMD gunicorn -c gunicorn.conf.py SJTUPlus.wsgi:application -
