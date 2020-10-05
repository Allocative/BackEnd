FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install python3-pip -y
COPY app /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"] 
