FROM python:3.12.6-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME=/home/roback
WORKDIR $APP_HOME

# Install libmagic for python-magic library
RUN apt-get update && apt-get install -y libmagic1

COPY requirements.txt $APP_HOME/requirements.txt

RUN pip install --no-cache-dir -r $APP_HOME/requirements.txt

COPY ./src $APP_HOME/src
COPY entrypoint.sh $APP_HOME/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c", "$APP_HOME/entrypoint.sh"]
