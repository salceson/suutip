FROM python:2.7
MAINTAINER "Michal Ciolczyk"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python database.py
ENTRYPOINT ["python"]
CMD ["service2.py", "--host", "0.0.0.0"]
