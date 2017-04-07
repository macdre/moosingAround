# Dockerfile for MCDA5570-Assignment02
# By: macdre

FROM ubuntu:16.04

# Update and install basic tools
RUN apt update && apt upgrade -y && apt install -y \
    vim \
    less \
    rsync \
    openssh-client \
    sshpass \
    curl \
    python3 \
    python3-dev \
    python3-pip

# Default to python3
RUN ln -s $(which python3) /usr/bin/python; exit 0

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

# Install the flask module
RUN pip3 install flask

# Install and configure the web app
COPY web-app.py /root/.
ENV FLASK_APP /root/web-app.py
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
EXPOSE 5000

# Run the flask on load
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]

