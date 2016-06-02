FROM ubuntu:latest
MAINTAINER "Michal Ciolczyk"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["service3.py", "--host", "0.0.0.0", "-u", "http://s2:5000", "-i", "http://s1:5000"]
