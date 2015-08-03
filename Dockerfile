FROM python:2

RUN apt-get update -y && apt-get dist-upgrade -y

# Apache Thrift for line support
# http://www.saltycrane.com/blog/2011/06/install-thrift-ubuntu-1010-maverick/
RUN apt-get install -y automake libtool flex bison pkg-config g++ libssl-dev make libqt4-dev git \
    debhelper cmake
RUN cd /tmp && curl http://archive.apache.org/dist/thrift/0.9.1/thrift-0.9.1.tar.gz | tar zx
RUN cd /tmp/thrift-0.9.1 && ./configure && make && make install
RUN rm -rf /tmp/thrift-0.9.1

# LINE python & patch to support login with email and password
# http://dev-program.com/how-to-use-line-api-in-python-lts-work/
RUN pip install line && pip uninstall -y line
RUN cd /tmp && git clone https://github.com/carpedm20/LINE.git
RUN cd /tmp/LINE/line && \
    wget https://gist.github.com/windows98SE/b739038218b6fe4d423f/raw/5f68cf3d9a2a88576b739810a6bd6fcaa0c5e940/api.py.patch && \
    patch api.py < api.py.patch
RUN cd /tmp/LINE && python config.py
RUN cd /tmp/LINE && python setup.py install
RUN rm -rf /tmp/LINE

# phatomjs drvier to selenium testing
RUN apt-get install -y cron
RUN echo "deb http://http.us.debian.org/debian unstable main non-free contrib" >> /etc/apt/sources.list  && apt-get update
RUN apt-get -t unstable install -y phantomjs

# mount code into docker and install python packages
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/mornitor-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/mornitor-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

CMD ["bash"]
