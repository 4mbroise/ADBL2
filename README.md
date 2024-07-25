# Assisted Debate Builder with Large Language Models: ADBL2

We introduce ADBL2, an assisted debate builder tool. It is based on the capability of large language models to generalise and perform relation-based argument mining in a wide-variety of domains. It is the first open-source tool that leverages relation-based mining for (1) the verification of existing relations in a debate and (2) the assisted creation of new arguments by means of large language models. ADBL2 is highly modular and can work with any open-source large language models that are used as plugins. As a by-product, we also provide the first [fine-tuned Mistral-7B large language model for binary relation-based argument mining available on Huggingface 🤗](https://huggingface.co/4mbroise/ADBL2-Mistral-7B), usable by ADBL2, which outperforms existing approaches for this task with an overall F1-score of 90.59% across all domains.

[See demo (v0.1)](https://youtu.be/KMzqKJlH9lE)

## How to start the application
Please use one of the docker-compose file :
 - **Start** `docker compose -f docker-compose-file.yml up` (in the background : `docker compose -f docker-compose-file.yml up --detach`
 - **Stop and remove** `docker compose -f docker-compose-file.yml down`
 - **Pull** (download latest docker image version) `docker compose -f docker-compose-file.yml down`

(Refer to docker compose files to know what url to seek to use de the UI or to query the API)

## Dev
![image](https://github.com/user-attachments/assets/814bf37a-a8c9-47f3-8bd0-c1cb0e5d5122)
This application is divided in three part : 
 - An LMQL server. It charges LLMs a applies constraints (directly managed in dockerfiles).
 - A FastAPI server. An HTTP interface to communicate withe the LMQL server (`backend` directory).
 - A React Web Interface (`adbl2` directory). 
