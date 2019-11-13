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
    You are now ready to start developing your api. Let's implement a first endpoint, and start the development server.
    
    


