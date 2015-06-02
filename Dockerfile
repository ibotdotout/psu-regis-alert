FROM python

RUN apt-get update
RUN apt-get install -y phantomjs

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
