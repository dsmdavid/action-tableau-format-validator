FROM python:3.8.2-buster

RUN apt-get update -yqq \
  && apt-get install -yqq \
    vim 

# upgrade pip
RUN pip install --upgrade pip

# Install dependencies:

WORKDIR /app

COPY ./src/requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

