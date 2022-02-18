# Contributing to `django-stomp-debug-callback`

## Lint

The use of `.pre-commit-config.yaml` [flake8](https://github.com/pycqa/flake8), [black](https://black.readthedocs.io/en/stable/), [isort](https://pycqa.github.io/isort/) and [pylint](https://pylint.org/) is required to the app development. 

You should always reformat your code before committing to the project.

## Test

Make sure to run all the tests before opening a pull request. Any new feature should also be tested!

## Sonar

We use [sonar](https://sonarcloud.io/) as a static code analyzer to look for improvements.

To test sonar local you can use the steps bellow.

1 - Run sonar server

To running the sonar server, just use the command:

`docker-compose up sonar`

And wait a few minutes for ElasticSearch, database, and other tools used by Sonar behind the scenes to be configured.

After uploading the server, we can access SonarQube at http://localhost:9000.

2 - Creating the project setup on the local Sonar Server

By default, the server uses the credentials below to login:
username: admin
password: admin

![step 1 sonar](docs/sonar-setup-1.png?raw=true)

When logging in for the first time, you will need to update your password. In order for us to be able to use the 
sonar-cli service added to docker-compose.yaml correctly, we must update the password to the value of the 
`SONAR_PASSWORD` variable, which in this case is set to test

![step 2 sonar](docs/sonar-setup-2.png?raw=true)

3 - Configure `juntossomosmais_django-stomp-debug-callback` project into sonar server.

After changes password we can see the initial screen below.

Let's click on the Add Project button
![step 4 sonar](docs/sonar-setup-4.png?raw=true)

choose option manually
![step 4 sonar](docs/sonar-setup-4.png?raw=true)

Insert the project key from `sonar-project.properties` in this project we can use `juntossomosmais_django-stomp-debug-callback`
![step 5 sonar](docs/sonar-setup-5.png?raw=true)

After the steps above we can see project configured in sonar server
![step 6 sonar](docs/sonar-setup-6.png?raw=true)

4 - Run `sonar-cli` and see sonar analysis.

To run the sonar-cli first we need to export the test and coverage metrics to be analyzed.

For this we can use the test service of docker compose or manually run the test command:

- docker: `docker-compose up tests` 
- manually execution: `pipenv tox`

After tests execution we can run `sonar-cli` using docker-compose using command 

`docker-compose up sonar-cli`

![step 7 sonar](docs/sonar-setup-7.png?raw=true)

We can see all analysis and fix the appointments before submitting the PR.


## Commits

The `commit` summary should be structured as [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) standard.

## Reviewing pull requests

The [pull request review](https://github.com/juntossomosmais/django-stomp-debug-callback/pulls) contributions should follow [conventional comments](https://conventionalcomments.org/) standard.

## Pull assignees and labels

When creating a new [pull request](https://github.com/juntossomosmais/django-stomp-debug-callback/pulls) you must set at least one `assignee` and one `label`.
