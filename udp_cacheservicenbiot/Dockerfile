FROM ubuntu:16.04
FROM python
COPY . /UDPService
WORKDIR /UDPService
RUN apt-get update
RUN apt-get install mono-complete -y
RUN pip install -r requirements.txt
EXPOSE 1121/udp
CMD python ./UDPService.py