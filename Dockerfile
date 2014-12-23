FROM dockerfile/python

RUN apt-get update
RUN apt-get install -y phantomjs

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["bash"]
