# Simple News Aggregator

## Description
The goal of this project is to make a simple News Aggregator that will take news from the large site but only these, who are currently in trend.

## How to run
1. The first thing you need to do is to install [docker|https://docs.docker.com/engine/install/] to your computer

2. Put your parameters into the .env file. You must put OpenAi api key if you want to calculate sentiment score for an article 

3. After the docker will be installed and .env file is filled you have to build it and run
```cmd
docker-compose up --build
```
This command will run all containers and for the first time may take a while to install all dependencies and images

## Links
|Link                  |                    Usage                          |
|----------------------|---------------------------------------------------|
|http://localhost:5556/|Flower web app for monitoring your worker and tasks|
|http://localhost:8000/docs|Fast API web app to test News Aggregator       |


