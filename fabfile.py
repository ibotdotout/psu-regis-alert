# http://www.fabfile.org/installing-1.x.html

# debian
# sudo apt-get install fabric

# osx
# pip install 'fabric<2.0'

# usage
# run with "fab -H <host> <func>"

from fabric.api import run, local, env


def backup_db():
    run('mkdir -p /root/backup')
    run("""docker exec -d psu-regis-alert_db_1 sh -c '"""
        """mkdir -p backup/db_$(date +%Y-%m-%d_%Hh%Mm) """
        """ && mongodump -d psuRegisAlert """
        """ -o backup/db_$(date +%Y-%m-%d_%Hh%Mm)'""")
    run('docker cp psu-regis-alert_db_1:/backup/ /root')
    local("rsync -r -e 'ssh -i {0}' {1}:/root/backup/ backup/"
          .format(env.key_filename[0], env.host_string))
