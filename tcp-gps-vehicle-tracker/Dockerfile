FROM python
ADD echo_server.py /
#RUN pip install pystrich
RUN apt-get update
RUN apt-get install net-tools iputils-ping -y
RUN apt-get install telnet -y
RUN pip install paho-mqtt
EXPOSE 6789
CMD [ "python","-u", "./echo_server.py" ]


