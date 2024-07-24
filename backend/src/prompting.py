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

def arg2Mistralprompt(arg1, arg2, relation=None):
    mistralPrompt =  "[INST]\n"
    mistralPrompt += "Argument 1 : " + arg1 + "\n"
    mistralPrompt += "Argument 2 : " + arg2 + "\n"
    mistralPrompt += "[/INST]\n"
    mistralPrompt += "Relation : "

    if relation != None:
        mistralPrompt += relation + "\n"
    
    return mistralPrompt

def zeroShot(topArgument, subArgument, promptTemplate):
    prompt = ""

    match promptTemplate:
        case "ChatML":
            prompt += arg2ChatML(topArgument, subArgument)

        case "Mistral":
            prompt = "<s>"
            prompt += arg2Mistralprompt(topArgument, subArgument)

    return prompt

def fixed4shots(topArgument, subArgument, promptTemplate):
    prompt = ""

    match promptTemplate:
        case "ChatML":
            for example in FIXED_EXAMPLES:
                prompt += arg2ChatML(example["arg1"], example["arg2"], example["relation"])
            prompt += arg2ChatML(topArgument, subArgument)

        case "Mistral":
            prompt = "<s>"
            for example in FIXED_EXAMPLES:
                prompt += arg2Mistralprompt(example["arg1"], example["arg2"], example["relation"])
            prompt += arg2Mistralprompt(topArgument, subArgument)

    return prompt