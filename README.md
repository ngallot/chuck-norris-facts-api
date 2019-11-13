# chuck-norris-facts-api
A sample REST api using the FastApi framework, exposing some Chuck Norris facts.

This project is the first of three labs sessions, part of the 9 hours module *Machine Learning: from idea to product* 
of the Post Masters [Big Data And Analytics](https://www.telecom-paris.fr/en/post-masters-degree/all-post-masters-degree/post-masters-degree-in-big-data) from [Telecom ParisTech](https://www.telecom-paris.fr/en/home).

### Project description
Here, we propose to build a demo RESTful api in Python, using the framework FastApi. We will cover topics like:
- Setting up the python development environment with virtualenv
- Dockerizing the project from the beginning
- Coding model classes with (included in FastApi)
- Making a data access layer to a fake database
- Implementing GET, POST, PATCH, DELETE endpoints with FastApi to interact with this database.

### Instructions

#### Minimal working code

- Get your developement environment ready by:
    - Creating a virtual environment:
    ```bash
    git clone git@github.com:ngallot/chuck-norris-facts-api.git
    cd chuck-norris-facts-api
    virtualenv -p path/to/your/python3.7 venv
    source venv/bin/acivate
    ```
    - Install the project dependencies: 
    ```bash
    pip install -r requirements.txt
    ```
    Depending on your IDE, you can now set up a proper development environment.

- Implement a first API endpoint, in a Docker container:
    - Switch to the branch feature/minimal_working_code
    ```bash
    git status # if this is not empty, then handle your local changes
    git checkout feature/minimal_working_code
    ```
    - Explore the code, essentially:
        - The structure of the Python code in the app folder
        - How we define the app object
        - The structure of the Dockerfile
    
    - Build the docker container:
    ```bash
    docker build -t chuck-norris-facts-api:latest --no-cache .
    ```
    
    - Start the development server:
    ```bash
    docker run -p 80:80 chuck-norris-facts-api:latest 
    # NB: you might have apps listening on port 80 already, you can kill them first using pkill.
    ```
    
    - Open a web browser to : localhost, and enjoy the Swagger doc!
    
    
- Usage of docker-compose:
When developing a service that connects to other services, docker-compose tool is extermely convenient to replicate
a production-like environment. You can define multiple services, based on different docker images.
    - Install: if you haven't installed docker-compose, follow the instructions [here](https://docs.docker.com/compose/install/).
    - Switch to the branch feature/docker_compose_setup: 
    ```bash
    git status # if this is not empty, then handle your local changes
    git checkout feature/docker_compose_setup
    ```
    Looks at the file docker-compose.yaml, everything is defined here. To launch the development server, run the command:
    ```bash
    docker-compose up --build
    ```

- Auto reload of the development server:
As of now, if we make changes to our source code, we have to rebuild the docker container 
(the docker engine will automatically detect that the COPY step needs to be re-run) and restart it.
It would be convenient that the server restarts automatically when the source code has changed instead. As a non compiled code, python allows that easily,
and usages of Docker volumes come handy here, to map directly the contents of your disk into the container.
To enable this:
    - Get the code for this feature:
    ```bash
    git checkout feature/server_auto_reload
    ```
    - Stop any running container (useful command:)
    ```bash
    docker kill $(docker ps -q)
    ```
    - Restart the service:
    ```bash
    docker-compose up --build
    ``` 
    - Now make any change to your source code (like adding a new blank line). You should see your server restarting automatically.
