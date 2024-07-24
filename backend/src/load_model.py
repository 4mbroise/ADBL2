#---CONFIG-------------------------------------------------------------------------------------------------

defautlArgs = {
    "cuda"  :   True,
}

llamaCppArgs = {
    "cuda"          :   True,
    "n_gpu_layers"  :   80,
    "n_ctx"         :   2048,
    # "verbose"       :   True,
}

#----------------------------------------------------------------------------------------------------

import lmql

def load_model_and_tokenizer(modelConfig):

    modelName = modelConfig["modelPath"]

    args = defautlArgs

    if modelConfig["modelType"] == "llamaCpp":
        modelName = "llama.cpp:" + modelName
        args = llamaCppArgs

    # if modelConfig["isLocal"]:
    #     modelName = "local:" + modelName

    return lmql.model(modelName, tokenizer=modelConfig["tokenizer"], endpoint="lmql:4000")
