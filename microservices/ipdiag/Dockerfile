FROM python:2.7
MAINTAINER "Michal Ciolczyk"
RUN apt-get update -y && apt-get install -y traceroute && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["service1.py", "--host", "0.0.0.0"]
