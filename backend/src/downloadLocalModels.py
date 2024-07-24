import urllib.request
import json

def show_progress(block_num, block_size, total_size):
    print(str(round(block_num * block_size / total_size *100,2))+"%", end="\r")

with open("./models_config.json") as modelsFile:
    models = json.load(modelsFile)

for model in models:
    modelData = models[model]
    if modelData["modelType"] == "llamaCpp":
        filename = modelData["downloadUrl"].split("/")[-1]
        print("Downloading "+filename+" : ")
        urllib.request.urlretrieve(modelData["downloadUrl"], "/models/"+filename, show_progress)
        print()