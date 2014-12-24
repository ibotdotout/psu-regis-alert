#!/bin/bash

pip install -r requirements.txt --use-mirrors
nosetests tests/unit
gunicorn route:app --log-file=- --pid=/tmp/regis-gunicorn.pid --daemon
pybot  -d /tmp --variable SERVER:"localhost:8000" tests/acceptance/
