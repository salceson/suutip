FROM ubuntu:latest
MAINTAINER "Michal Ciolczyk"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential iputils-ping inetutils-traceroute
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["service1.py", "--host", "0.0.0.0"]
