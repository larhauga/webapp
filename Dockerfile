FROM ubuntu:14.04
MAINTAINER Lars Haugan <lars@larshaugan.net>
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q curl python-all python-pip wget build-essential
ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp
ADD requirements.txt /opt/webapp/
RUN pip install -r requirements.txt
EXPOSE 2020
CMD ["python", "webapp.py", "-p", "2020"]
