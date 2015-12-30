# Fix env with space
# http://unix.stackexchange.com/a/196761

IFS='
'

#env - `cat /root/env.sh` $1 >> /var/log/cron.log 2>&1
env - `cat /root/env.sh` $1
