from prompting import fixed4shots, zeroShot


async def relationsClf(model, topArgument, subArgument, promptTechnique, promptTemplate):
    prompt = None

    if promptTechnique == "fixed-4-shots":
        prompt = fixed4shots(topArgument, subArgument, promptTemplate)
    if promptTechnique == "0-shot":
        prompt = zeroShot(topArgument, subArgument, promptTemplate)
    
    score = await model.score(prompt, ["attack", "support"])

    res = dict(zip(["attack", "support"], score.probs()))
    res["prompt"] = prompt

    return res