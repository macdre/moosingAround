api: gunicorn --chdir ./src/py app:app -b 127.0.0.1:9090 --log-file - --error-logfile -&
web: node --optimize_for_size --max_old_space_size=256 server.js