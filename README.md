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
    
    


