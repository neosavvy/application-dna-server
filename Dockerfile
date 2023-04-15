FROM python:3.9
EXPOSE 9080
ENV PYTHONUNBUFFERED True

WORKDIR /app

RUN apt update
RUN apt install curl

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

#RUN python -c "import nltk; nltk.download('punkt')"

COPY . .