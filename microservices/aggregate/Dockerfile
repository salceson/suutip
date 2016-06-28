FROM python:2.7
MAINTAINER "Michal Ciolczyk"
WORKDIR /app
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD *.py ./
CMD ["python", "aggregate.py", "--host", "0.0.0.0"]
