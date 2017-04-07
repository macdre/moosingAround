# Assignment 02 for MCDA 5570
## By: Ross MacDonald
### This README explains how to use the provided Dockerfile and flask python web app

#### Clone the repo: 
First, clone the git repo into an empty local directory
```
cd <myworkspace>
mkdir docker-web-app
cd docker-web-app
git clone git://blalbhalbha/
```

#### Build Docker Image 
Next, build an image based on the provided dockerfile:
    docker build -t <image-name> .

#### Run Docker Container
Next, run the built image:
    docker run -d -P --name <container-name> -it <image-name>

The container will expose a port to docker, check to see what that is:
    docker port <container-name>

Note the port that docker has exposed, it will follow the 0.0.0.0 IP.
For example, we will use 32768 in this example docker port output:
    5000/tcp -> 0.0.0.0:32768 

#### Test the Flask
Now you can test the web app by running:
    curl http://127.0.0.1:<port>/hello

Note, if your connection is rejected, you should confirm the IP that docker is assigning to your application by running the following command:
    docker-machine ip

#### Debugging
To check on the application, you can log into the container like so:
    docker exec -it <container-name> bash
