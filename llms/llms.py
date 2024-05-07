from matplotlib import pyplot as plt
import numpy as np
import streamlit as st
import lmql
import asyncio

FIXED_EXAMPLES = [
    {
        "arg1" : "Even in the case of provocateurs, it can be an effective strategy to call their bluff, by offering them a chance to have a rational conversation. In this case, the failure to do so is their responsibility alone.",
        "arg2" : "No-platforming hinders productive discourse.",
        "relation" : "attack"
    },  
    {
        "arg1" : "A country used to receiving ODA may be perpetually bound to depend on handouts (pp. 197).",
        "arg2" : "Government structures adapt to handle and distribute incoming ODA. As the funding from ODA is significant, countries have vested bureaucratic interest to remain bound to aid (pp. 197).",
        "relation" : "support"
    },
    {
        "arg1" : "Elections would limit the influence of lobbyists on the appointment of Supreme Court judges.",
        "arg2" : "The more individuals take part in a decision, as would be the case in a popular vote compared to a vote in the Senate, the harder it is to sway the outcome.",
        "relation" : "support"
    }, 
    {
        "arg1" : "ChatGPT will reach AGI level before 2030.",
        "arg2" : "To reach AGI it should be able to generate its own goals and intentions: where would it draw these from?",
        "relation" : "attack"
    }
]

def loadModel():
    # print("Load model")
    # print(st.session_state.llm_choice)
    match st.session_state.llm_choice["modelType"]:
        case "transformers":
            loadHFModel()
        case "llamaCpp":
            loadLlamaCppModel()

def loadHFModel():
    modelPath       = st.session_state.llm_choice["modelPath"]
    modelTokenizer  = st.session_state.llm_choice["tokenizer"]
    isLocal         = st.session_state.llm_choice["local"]

    if isLocal:
        # print("isLocal")
        st.session_state["llm_model"] = lmql.model("local:"+modelPath, cuda=True)
    else:
        st.session_state["llm_model"] = lmql.model(modelPath, cuda=True)

def loadLlamaCppModel():

    # print("load llamaCpp model")

    modelPath       = st.session_state.llm_choice["modelPath"]
    modelTokenizer   = st.session_state.llm_choice["tokenizer"]

    llamaCppArgs = {
        "cuda"          :   True,
        "n_gpu_layers"  :   80,
        "n_ctx"         :   2048,
        # "verbose"       :   True,
    }

    # print("local:llama.cpp:"+modelPath)

    st.session_state["llm_model"] = lmql.model(
        "local:llama.cpp:"+modelPath, 
        tokenizer=modelTokenizer, 
        **llamaCppArgs,
    )


@lmql.query(decoder="argmax")
def queryFewShotsMistral(arg1, arg2):
    '''lmql
    """<s>[[INST]]
    Argument 1 : Even in the case of provocateurs, it can be an effective strategy to call their bluff, by offering them a chance to have a rational conversation. In this case, the failure to do so is their responsibility alone.
    Argument 2 : No-platforming hinders productive discourse.
    [[/INST]]
    Relation : attack
    [[INST]]
    Argument 1 : A country used to receiving ODA may be perpetually bound to depend on handouts (pp. 197).
    Argument 2 : Government structures adapt to handle and distribute incoming ODA. As the funding from ODA is significant, countries have vested bureaucratic interest to remain bound to aid (pp. 197).
    [[/INST]]
    Relation : support
    [[INST]]
    Argument 1 : Elections would limit the influence of lobbyists on the appointment of Supreme Court judges.
    Argument 2 : The more individuals take part in a decision, as would be the case in a popular vote compared to a vote in the Senate, the harder it is to sway the outcome.
    [[/INST]]
    Relation : support
    [[INST]]
    Argument 1 : ChatGPT will reach AGI level before 2030.
    Argument 2 : To reach AGI it should be able to generate its own goals and intentions: where would it draw these from?
    [[/INST]]
    Relation : attack
    [[INST]]
    Argument 1 : {arg1}
    Argument 2 : {arg2}
    [[/INST]]
    Relation : [RELATION]""" distribution RELATION in set(["attack", "support"])
    '''


def relationsClf(node, newArgument):

    print("test")

    #import nest_asyncio
    #nest_asyncio.apply()

    prompt = None

    if node.tree == "1.":
        node.toneInput = node.subject

    if st.session_state.inf_technique == "Fixed 4-Shots":
        prompt = fixed4shots(node, newArgument)
    if st.session_state.inf_technique == "0-Shot":
        prompt = zeroShot(node, newArgument)

    print(prompt)
    
    result = queryFewShotsMistral(node.toneInput, newArgument, model=st.session_state["llm_model"])
    score = lmql.score_sync(prompt, ["attack", "support"], model=st.session_state["llm_model"])

    # print(prompt)

    return dict(zip(["attack", "support"], score.probs())), prompt




def fixed4shots(node, newArgument):
    prompt = ""

    match st.session_state.llm_choice["promptTemplate"]:
        case "ChatML":
            for examples in FIXED_EXAMPLES:
                prompt += arg2ChatML(examples["arg1"], examples["arg2"], examples["relation"])
            prompt += arg2ChatML(node.toneInput, newArgument)

        case "Mistral":
            prompt = "<s>"
            for examples in FIXED_EXAMPLES:
                prompt += arg2Mistralprompt(examples["arg1"], examples["arg2"], examples["relation"])
            prompt += arg2Mistralprompt(node.toneInput, newArgument)

    return prompt

def zeroShot(node, newArgument):
    prompt = ""

    match st.session_state.llm_choice["promptTemplate"]:
        case "ChatML":
            prompt += arg2ChatML(node.toneInput, newArgument)

        case "Mistral":
            prompt = "<s>"
            prompt += arg2Mistralprompt(node.toneInput, newArgument)

    return prompt


def arg2ChatML(arg1, arg2, relation=None):
    chatml =  "[[INST]]\n"
    chatml += "Argument 1 : " + arg1 + "\n"
    chatml += "Argument 2 : " + arg2 + "\n"
    chatml += "\n"
    
    chatml += "<|im_start|>assistant\n"
    chatml += "Relation : "

    if relation != None:
        chatml += relation + " \n"
    
    return chatml


    # <s>[[INST]]
    # Argument 1 : {arg1}
    # Argument 2 : {arg2}
    # [[/INST]]

def arg2Mistralprompt(arg1, arg2, relation=None):
    mistralPrompt =  "[INST]\n"
    mistralPrompt += "Argument 1 : " + arg1 + "\n"
    mistralPrompt += "Argument 2 : " + arg2 + "\n"
    mistralPrompt += "[/INST]\n"
    mistralPrompt += "Relation : "

    if relation != None:
        mistralPrompt += relation + "\n"
    
    return mistralPrompt



# Argument 1 : Even in the case of provocateurs, it can be an effective strategy to call their bluff, by offering them a chance to have a rational conversation. In this case, the failure to do so is their responsibility alone.
# Argument 2 : No-platforming hinders productive discourse.
# 
# <|im_start|>assistant
# Relation : attack
# [[INST]]
# Argument 1 : A country used to receiving ODA may be perpetually bound to depend on handouts (pp. 197).
# Argument 2 : Government structures adapt to handle and distribute incoming ODA. As the funding from ODA is significant, countries have vested bureaucratic interest to remain bound to aid (pp. 197).
# 
# <|im_start|>assistant
# Relation : support
# [[INST]]
# Argument 1 : Elections would limit the influence of lobbyists on the appointment of Supreme Court judges.
# Argument 2 : The more individuals take part in a decision, as would be the case in a popular vote compared to a vote in the Senate, the harder it is to sway the outcome.
# 
# <|im_start|>assistant
# Relation : support
# [[INST]]
# Argument 1 : ChatGPT will reach AGI level before 2030.
# Argument 2 : To reach AGI it should be able to generate its own goals and intentions: where would it draw these from?
# 
# <|im_start|>assistant
# Relation : attack
# [[INST]]
# Argument 1 : {arg1}
# Argument 2 : {arg2}
# 
# <|im_start|>assistant
# Relation : [RELATION]""" where RELATION in set(["attack", "support"])

def scorePlot(score, legend=True):
    category_names = ['Attack', 'Support']

    results = {
        'scores' : [round(score["attack"]*100,1),round(score["support"]*100, 1)]
    }

    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1])
    )

    fig, ax = plt.subplots(figsize=(4, 1))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.axis('off')
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    if legend:
        ax.legend(ncols=1, bbox_to_anchor=(1, 0),
            loc='lower left', fontsize='small', frameon=False)

    return fig, ax