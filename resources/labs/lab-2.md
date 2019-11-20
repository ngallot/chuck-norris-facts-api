# Lab 2 - Deploying the api on Google Cloud Run

#### Setting up the GCP project
To execute this step, you should have a google cloud platform account, and a working gcloud command.

First, create a new project on the Google Cloud platform console by logging into the console. Call this project cnf-api-production.

After your project has been created, you should have something like this: 

<p align="center">
  <img src="../img/gcp_project.png" alt="GCP Console" />
</p>

#### Enabling necessary API's
For this project to work properly, we need to activate several api's on Google Cloud Platform:

- [Identity Access Management](https://cloud.google.com/iam/docs/reference/rest) (iam.googleapis.com)
- [Cloud resource manager](https://cloud.google.com/resource-manager/docs/apis) (cloudresourcemanager.googleapis.com): 
- [Google Container Registry]() (containerregistry.googleapis.com)
- [Google Cloud Run](): (run.googleapis.com)

