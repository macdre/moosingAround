#!/bin/sh
if [ $APPLICATION_TYPE = 'WEB' ]
then
    node --optimize_for_size --max_old_space_size=256 server.js
elif [ $APPLICATION_TYPE = 'API' ]
then
    gunicorn --chdir ./src/py app:app --log-file - --error-logfile -
fi
