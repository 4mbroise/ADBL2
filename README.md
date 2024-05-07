# Assisted Debate Builder with Large Language Models: ADBL2

We introduce ADBL2, an assisted debate builder tool. It is based on the capability of large language models to generalise and perform relation-based argument mining in a wide-variety of domains. It is the first open-source tool that leverages relation-based mining for (1) the verification of existing relations in a debate and (2) the assisted creation of new arguments by means of large language models. ADBL2 is highly modular and can work with any open-source large language models that are used as plugins. As a by-product, we also provide the first [fine-tuned Mistral-7B large language model for relation-based argument mining](https://huggingface.co/4mbroise/ADBL2-Mistral-7B), usable by ADBL2, which outperforms existing approaches for this task with an overall F1-score of 90.59% across all domains.

[See demo](https://youtu.be/KMzqKJlH9lE)

## How to

### Install requirements
`pip install -r requirements.txt`

### Start the App
Serve the local web server using the command `streamlit run app.py`

### Configure your ADBL2 instance to use your LLMs 
Please adapt the configuration file **models.json** to your configuration
  
