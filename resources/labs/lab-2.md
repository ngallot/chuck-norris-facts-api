# Lab 2 - Deploying the api on Google Cloud Run

#### Setting up the GCP project
To execute this step, you should have a google cloud platform account, and a working gcloud command.

First, create a new project on the Google Cloud platform console by logging into the console. Call this project *_cnf-api-production_*.

After your project has been created, you should have something like this: 

<p align="center">
  <img src="../img/gcp_project.png" alt="GCP Console" />
</p>

#### Installing the gcloud command line tool
To interact with Google Cloud Platform resources, you can use the Google Cloud Sdk. It includes 
a command line tool named gcloud.
I suggest you first follow the steps in the [quickstart](https://cloud.google.com/sdk/docs/quickstarts)*[]: 


#### Setting up the gcloud command to interact with our project
Let's run the below commands (1 by 1...) to set up the gcloud command line to be able to take actions on our project:

```bash
gcloud auth login       # Will open a web browser to enable google authentication
gcloud projects list    # Will list the projects associated to your account. Please write down the id (PROJECT_ID) of your project cnf-api-production.


# Setting up gcloud to interact with the cnf-api-production project
export PROJECT_ID=xxx   # The id of the project you just got from the previous step
export REGION=europe-west2-b

gcloud config list      # To see the current configuration of your gcloud command line
gcloud config set project ${PROJECT_ID} # To set the project to interact with
gcloud config set run/region ${REGION} # To set the default region to use for Cloud Run
```

#### Enabling necessary API's
For this project to work properly, we need to activate several api's on Google Cloud Platform:

- [Identity Access Management](https://cloud.google.com/iam/docs/reference/rest) (iam.googleapis.com)
- [Cloud resource manager](https://cloud.google.com/resource-manager/docs/apis) (cloudresourcemanager.googleapis.com): 
- [Google Container Registry](https://cloud.google.com/container-registry/) (containerregistry.googleapis.com)
- [Google Cloud Run](https://cloud.google.com/run/): (run.googleapis.com)

We can do this through the gcp console, or directly with the gcloud command line tool. Let's do it with gcloud (doc [here](https://cloud.google.com/sdk/gcloud/reference/services/enable)):
```bash
# Check the list of available services for our project:
gcloud services list --available

# Activate our 4 necessary apis:
gcloud services enable iam.googleapis.com cloudresourcemanager.googleapis.com containerregistry.googleapis.com run.googleapis.com --async

```

#### Deploying our API
Now that we've enabled the necessary apis, we can push our Docker container to Google Container Registry. It is a private Docker container registry,
working like a private DockerHub registry.


##### Pushing our docker container to Google Container Registry
First, we need to authenticate Docker before pushing the image to our private registry. We can use gcloud for that: 
```bash
gcloud auth configure-docker
```

Then, we need to give a special tag to our Docker image, to tell docker to push it to our private registry. Let's call our image cnf-api-production,
because  will deploy the production environment. The :latest means that it's the latest version. We could also put a semantic version here.
```bash
export DOCKER_TAG=gcr.io/${PROJECT_ID}/cnf-api-production:latest

docker build -t ${DOCKER_TAG} --build-arg config_file=production.ini . # NB: this step is not mandatory if we've already built the image with another tag. We could just add a new tag to the image.

```

And let's just push!
```bash
docker push ${DOCKER_TAG}
```

If you go to the gcp console and check out your images in the cloud container registry, you should see something like this:
<p align="center">
  <img src="../img/gcloud_container_image.gif" alt="GCP Cloud Container Registry" />
</p>

##### Setting up a container on Google Cloud Run
We're almost there, we just now need to deploy our image into a working container. This is where we'll use Google Cloud Run: a serverless architecture to run
docker images.

First, make sure that you've created the file env-vars/production.env, with contents ENV=production
The command
```bash
env_vars=$(cat env-vars/production.env  | paste -sd "," -)
```
will read this file, and extract its contents, separated by commas. This is the format gcloud expects when setting environment variables for a cloud run container.


```bash
export SERVICE_NAME=chuck-norris-facts-api
export ENV_VARS=$(cat env-vars/production.env  | paste -sd "," -)

gcloud beta run deploy ${SERVICE_NAME} \
    --image ${DOCKER_TAG} \
    --set-env-vars=${ENV_VARS} \
    --region europe-west1 \
    --platform managed \
    --allow-unauthenticated \
    --memory 1G
```

And voila! Our API is now available in the cloud, and it's not costing anything when not running. The gcloud command we just ran will
output the url where our api has been deployed. You can test it by executing an http request:
```bash
export API_URL=xxx # the value of the deployed url, returned by the gcloud command.
curl -X GET ${API_URL}/facts/ # will return all facts in our database
```


#### Deploying changes automatically: continuous deployment
In this section, we will see that we can do better than deploying our api manually. We will use
Circle CI to help us doing it automatically for us.
The very basic concept is that here, we've executed a list of commands manually to deploy our application.
Why not doing it automatically? After all it's just a set of bash commands to run. We can do this with Circle CI, by describing the list
of commands to be run when our GitHub repository changes, and they are automatically triggered.
Behind the hood, when the repo changes, and a trigger has been configured to take actions, Circle CI will:
- Start a VM in their own cloud
- Execute a list of actions that we will have configured in the Circle CI configuration file
- Stop the machine.

And all this comes for free with the Circle CI basic plan.


##### Making minimal configuration
Circle CI works with configuration files. Basically, this configuration file, in the yaml format (same as docker-comopose file), 
describes a list of actions to be taken by the machine executing it on Circle CI cloud. Let's build a minimal configuration, 
just to enable setting up the CI for our project:

- First: create a new branch called feature/minimal_ci
```bash
git checkout -b feature/minimal_ci
```

Then create a directory to host the circle ci configuration and create an empty config file:
```bash
mkdir .circleci
touch .circleci/config.yml
```

Add the below contents to the .circleci/config.yml:
```yaml
version: 2.0
jobs:

  helloci:
    working_directory: ~/repo
    docker:
    - image: google/cloud-sdk:slim
    steps:
    - checkout
    - run:
        name: Say Hello
        command: |
          echo Hello Circle CI!


workflows:
  version: 2
  say-hello-to-ci:
    jobs:
    - helloci
```

We define here a dummy job, outputting "Hello Circle CI" on the console. It will first pull the google/cloud-sdk:slim Docker image, then 
checkout our code, and finally run our Say Hello command.

Then push your changes, and merge this branch to master:
```bash
git status
git add .circleci
git commit -m 'minimal working configuration'
git push

git checkout master
git pull
git merge feature/minimal_ci
git push
```


##### Setting up Circle CI to interact with your project
The first step here, after creating an account on CircleCi, is to setup your project.

For that, go to the CircleCI console, and click ADD PROJECTS. Select your GitHub chuck-norris-facts-api project, then go directly 
to "start building". You can still read the instructions, but we will setup the configuration ourselves.

<p align="center">
  <img src="../img/setup_ci.gif" alt="Circle CI follow project" />
</p>

You're done! You can now start to enjoy automated builds!

##### Writing a real Circle CI configuration file
NOw that we've demonstrate how to write a dummy circle ci config file, triggering actions from GitHub, let's implement the steps we've ran manually to deploy our app.

##### The unit tests step
If we follow the git-flow process described in week 1, we know that:
- we should not push code directly to protected branches (ie branches that are deployed in a proper environment)
- we should run unit tests to check that we did not break anything in the code



#### Next steps
In this lab we've shown how to automate the deployment of our app, on a specific cloud infrastructure: Google Cloud Run.
If you want to explore further, some ideas could be: 
- Deploying a development and staging environment: because here we only have a production environment and it's clearly not enough for a real case scenario.
- Deploy to another cloud infrastructure: Google Cloud Run is great for our needs, but could be limited for other use cases. You could want to 
deploy somewhere else
- Explore the possibility to add artifacts to your builds on Circle CI:
    - tests reports
    - test coverages
    - ...
 Have fun building!
 