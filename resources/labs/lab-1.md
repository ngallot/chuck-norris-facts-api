# Lab 1 - Making an API working locally

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
- Check out the branch containing minimal working code: 
```bash
git checkout feature/minimal_working_code
```

- Implement a first API endpoint, in a Docker container:
    - Explore the code, essentially:
        - The structure of the Python code in the app folder
        - How we define the app object
        - The structure of the Dockerfile
    
    - Build the docker container (go [there](####troubleshooting) if this command is failing):
    ```bash
    docker build -t chuck-norris-facts-api:latest --no-cache .
    ```
    
    - Start the development server:
    ```bash
    docker run -p 80:80 chuck-norris-facts-api:latest 
    # NB: you might have apps listening on port 80 already, you can kill them first using pkill.
    ```
    
    - Open a web browser to : localhost, and enjoy the Swagger doc!

    
#### Usage of docker-compose:
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

#### Auto reload of the development server:
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

#### App configuration and environment variables:
Often, there are common configurations / settings for our application that we do not want to hardcode. It is especially useful when we use different environments.
For example, if we connect to a database to retrieve data, we might want to make queries against different database instances if we are running the development code or the
production code. Imagine you are implementing a DELETE endpoint in your API, connecting to a backend database. It means you will have to run a DELETE sql query against this database, while you are developing your feature.
You obviously don't want to run this against the production database. Hence, it is useful to have a local environment, where the database connection string points to a local database,
and a production environment for the deployed api, where the database connection string points to the production database. This is where configurations are useful.
To get the code implementing this feature: 
- Run: 
```bash
git checkout feature/configuration
```
- Check the file: 
```bash
config/local.ini
```
For now, it contains only 1 section, named [APP], with basic info about our app. local.ini means that this is the configuration file
that we will use for local development. Other configuration files can come later, if we decide to manage multiple environments.

- Check the code source code changes in the below files to understand how we have implemented the python code to parse this configuration file. 
It is using the configparser library, available in the python standard library:
```bash
app/__init__.py # Notice that we are parsing the configuration file in __init__.py, to make it available anywhere in the code.
app/config.py   # Notice that in line 68, the code expects an environment variable named ENV.
app/main.py     # We are importing the parsed configuration, and we use it to create our FastApi object.
```

- Create a the environment variable file:
Because environment variables **should not be commited in git**, you have to manually create the environment variables directory and save the environment variable files inside.
To share this file, you can have several options:
    - a separate GitHub repo
    - a password manager allowing to share files
    - a google drive like system
    - a dedicated credentials management system
    - etc...

To create this file:
```bash
mkdir env-vars
touch env-vars/local.env
echo ENV=local > env-vars/local.env
```
You can also note that the .gitignore file has been updated to ignore all *.env files in the project.

- Check the changes in the container setup to see how this configuration has been integrated:
```bash
Dockerfile:         # We have added an extra step to copy the configuration files in the container
docker-compose.yaml # We have added en env_file argument to specify to the docker engine which environment variables need to be made available to the container.
```

#### Logging
Like said in the lecture, using print() statements everywhere in the code is quite dirty. There are much better things to do, starting by using
the built-in library [logging](https://docs.python.org/3/library/logging.html)
To check how this has been implemented:
- Checkout the corresponding branch:
```bash
git checkout feature/logging
```
The below files have been modified: 
```bash
- config/local.ini          # Here, we added a new configuration section called [LOGGING] defining the logging level and formatting options.
- app/config.py             # Python code to parse the newly added LOGGING section
- app/logging_utils.py      # Code to build a new logger with correct formatting based on config values
- app/main.py               # Instantiate a logger in the main file and add a logging message after server start.
```

Once you've pulled those changes, your server should automatically restart, and you should see a nice logging message in the console: 
```bash
2019-11-13 21:18:22,940:app.main:INFO:Chuck Norris Facts API local server started successfully.
```
 
#### Database access
In this section, we implement a **fake** database. It's just an in-memory dictionary, and will be used like a real database for the purpose of this demo.
In a real case scenario, the database would be a real one, hosted on its own server, with CRUD operations implemented (via SQL queries for instance).
To get the code related to this implementation:
- Run the command: 
```bash
git checkout feature/database_access
```

- Files changed:
```bash
app/db.py
```
In this file , we've added contents to the fake database, as well as methods to retrieve, insert, update and delete an objects.
     
#### Implementing the first api endpoints
Once we have implemented our database access layer, we can now expose REST endpoints to interact with this database. The first endpoints we will implement are the GET endpoints,
to retrieve resources from the database, given certain criteria.
To retrieve the code implementing this feature, run the command:
```bash
git checkout feature/get_endpoints
```

There are quite a lot of changes in the code for this branch, let's have a closer look at what's new:
-   Model classes: 
    In the file _app/models.py_, we define the data model for our first endpoints. The classes are derived from Pydantic's BaseModel class.
    We define here a base class for our chuck norris facts, containing the fact itself as a string, and a derived class containing also the database id.
    The schema is very simple and straight forward. Note that when we define the class: 
    ```python
    class ChuckNorrisFactBase(BaseModel):
        fact: str = Schema(default=..., title='fact', description='The Chuck Norris Fact')
    ```
    It is not mandatory to defne a Schema, as Pydantic will already interpret the type hints (: str) and handle data validation automatically. However, it is very useful to
    define those Schema for the Swagger doc built by FastApi. You can check out your Swagger UI to see that the description is written in the generated doc.
-   Database access:
    Here, we've just defined methods to access to a list of facts, given their ids.
-   Main file: _main.py_
    Here we have implemented 2 new endpoints, to illustrate 2 usages of GET endpoints:
    - A first endpoint querying the database for a given id:
    ```python
    @app.get('/fact/{fact_id}', description='Retrieve a Chuck Norris fact from its id',
             response_model=models.ChuckNorrisFactDb, tags=['Facts'])
    ``` 
    There is only 1 mandatory argument, that according to RESTful apis design best practices, we should put directly in the url.
    FastApi handles that easily, you just have to define it in the path of the operation and it will automatically be transmetted to the python function executing your operation.
    Note that when we do not find the fact in database, we want to raise a clear HTTP exception with correct status code. So that clients connecting to our api will be able to handle this
    status code according to their needs.
    - A second endpoint querying the database for a list of ids:
    ```python
    @app.get('/facts/', description='Retrieve Chuck Norris facts from the database. Optional filter on the ids to '
                                    'retrieve.', response_model=List[models.ChuckNorrisFactDb], tags=['Facts'])
    ```
    Here the design is different. We can provide an argument for this operation, but it is not given directly in the url. It is defined in the python function that handles the request:
    ```python
    def get_facts(ids: List[int] = Query(
        default=None, title='ids', description='The list of ids to retrieve')) -> List[models.ChuckNorrisFactDb]:
    ```
    The _default=None_ means that the parameter ids, defined as a query parameter, means that this parameter is optional. When you check the Swagger UI doc, mandatory params have a red star next to them,
    optional params don't.
    NB: even if this parameter is defined in the python function handling the request, it's purely a FastApi trick. If you test the endpoint from the swagger doc directly, with ids 1 and 11,
    you will see a log message like this (see how the ids are appended at the end of the url):
    ```bash
    2019-11-14 07:27:25,311:uvicorn:INFO:('192.168.96.1', 54704) - "GET /facts/?ids=1&ids=11 HTTP/1.1" 200
    ```

#### Writing unit tests
Now that we have implemented a few endpoints, it is now time to write unit tests. The main purpose of unit testing is to make sure that we are not breaking the code when making changes.
changes. It also makes sure that the code is doing what we expect. Reading unit tests usually gives a good understanding of how the app should behave.
To do that, we will use the built-in unittests library, along with pytest to run the tests.
To check the code and run the unit tests:
- Get the test branch: 
```bash
git checkout feature/unit_tests
```
- CHeck the files changed:
```bash
app/config.py
test-requirements.txt
tests/
```
- Create a dedicated virtual env for running tests:
```bash
virtualenv -p path/to/my/python3.7 venv_test
source venv_test/bin/activate 
```

- Install the test requirements:
```bash
pip install -r test-requirements.txt
```
NB: it is interesting to note that you can reference other requirements.txt files within a requirements.txt. For instance, test-requirements.txt is referencing requirements.txt
and just adding an extra dependency to pytest.

- Run the tests:
```bash
export ENV=test && pytest tests/app_tests.py
```
This should result in 3 successful tests (eventually with warnings).

- Zoom on the test code:
Everything lies in the file _tests/app_tests.py_. Notice that we have modified the file app/config.py to allow an extra environment named 'test', with its own .ini file.
Then, we use the test client provided by starlette framework (the web server framework FastApi is based on):
```python
from starlette.testclient import TestClient
from app.main import app
from app.models import ChuckNorrisFactDb

client: TestClient = TestClient(app)
```
Here, we build a fake client that behaves exactly like the requests library. It manages directly requests against our endpoints, without needing to start a server and make
http requests to it. It is then very convenient to test the whole application.
Then in the tests, implemented in the class AppTests, we are testing 3 things:
- The endpoint to retrieve a fact given its id returns a successful response when the id exists in DB
- The same endpoint sends an 'not found' error when requesting an id which does not exist in DB
- The endpoint to retrieve all facts returns the whole contents of the db.

Those tests can be enhanced, and more expected behaviours can be tested. Of course, a test like the test_get_all_facts should never be written against a real database,
because it will return all the contents... It's just for demo here :-)

#### Next steps
Time to write your own code now!
For next week, I'm asking you to implement new endpoints to our API.
- 1 endpoint POST, which takes a json containing a list of facts (strings) as input, and returns a list of database facts (id and fact) as output. Check out the [doc](https://fastapi.tiangolo.com/tutorial/body/) to help you,
even though all BaseModel classes have already been written.

- 1 endpoint PATCH, that will take a json containing database facts (id, fact), to be updated. It should return the updated objects.
NB: the endpoint should output a clear error message and status code if an id not present in the database is given in the request.

- 1 endpoint DELETE: to delete a list of facts given their ids.

- Unit tests to go with those new endpoints!


#### TROUBLESHOOTING

##### docker commands failing
If you have an error while running the docker command, it might be because of insufficient privileges. To fix this, apply
the steps described [here](https://docs.docker.com/install/linux/linux-postinstall/) or [here](https://github.com/sindresorhus/guides/blob/master/docker-without-sudo.md)

##### docker-compose commands failing
If the docker-compose commands are failing, it might be:
- Because of docker commands failing (docker-compose is using docker engine in the background), so see step 1.
- Because your version of docker-compose is too old to support the docker-compose.yaml file version. To fix that, checkout the docs to install the latest
version of docker-compose. I've already downgraded the docker-compose file version from 3.7 to 3.1 so it should work for most of your configurations.


  