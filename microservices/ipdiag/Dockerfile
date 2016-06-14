FROM python:2.7
MAINTAINER "Michal Ciolczyk"
RUN apt-get update -y && apt-get install -y traceroute && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
WORKDIR /app
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD *.py ./
ENTRYPOINT ["python"]
CMD ["ipdiag.py", "--host", "0.0.0.0"]
