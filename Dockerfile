FROM python:slim
WORKDIR /root

COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN mkdir log && touch log/error.log && touch log/access.log
COPY ./ ./

CMD ./run.sh
