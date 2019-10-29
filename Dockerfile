from ubuntu:latest

RUN apt-get update
RUN apt-get -y install git
RUN apt-get -y install unixodbc unixodbc-dev
RUN apt-get -y install python3-dev && apt-get -y install python3-pip && pip3 install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000
ENV FLASK_ENV=development 
ENV FLASK_APP=flaskr
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
CMD ["flask", "run", "--host=0.0.0.0"]


