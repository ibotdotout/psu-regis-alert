FROM dockerfile/python
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
