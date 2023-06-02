From alpine:latest

ENV APP_HOME "/app"
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY config.py $APP_HOME/
COPY main.py $APP_HOME/
COPY mblog_api.py $APP_HOME/
COPY requirements.txt $APP_HOME/
COPY telegram_api.py $APP_HOME/

RUN apk update
RUN apk add python3
RUN apk add py3-pip
RUN python3 -m pip install -r requirements.txt

CMD ["python3", "main.py"]
