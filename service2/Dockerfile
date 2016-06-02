FROM ubuntu:latest
MAINTAINER "Michal Ciolczyk"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python database.py
ENTRYPOINT ["python"]
CMD ["service2.py", "--host", "0.0.0.0"]
