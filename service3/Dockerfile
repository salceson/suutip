FROM python:2.7
MAINTAINER "Michal Ciolczyk"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["service3.py", "--host", "0.0.0.0", "-u", "http://s2:5000", "-i", "http://s1:5000"]
