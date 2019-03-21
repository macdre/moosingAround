web: gunicorn --chdir ./src/py app:app -b 0.0.0.0:8080 --log-file -
web: node --optimize_for_size --max_old_space_size=256 server.js