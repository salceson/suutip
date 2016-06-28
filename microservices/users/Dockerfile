FROM python:2.7
MAINTAINER "Michal Ciolczyk"
WORKDIR /app
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD wait-for-it.sh /usr/local/bin/wait-for-it.sh
ADD *.py ./
CMD ["python", "users.py", "--host", "0.0.0.0"]
