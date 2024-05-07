import sys, time, json, re
from anytree import Node, RenderTree
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter

sys.setrecursionlimit(100000)

def group_arguments(tableau):
    argGroup = tableau[0]
    i = 1

    while True:

        if i > len(tableau) - 1:
            return [argGroup]

        stance = re.search(r"(Con|Pro)(?::)", tableau[i])
        if stance == None:
            argGroup = argGroup + " " + tableau[i]
            i+=1
        else:
            return [argGroup] + group_arguments(tableau[i:]) 

    """
    if len(tableau) % 2 != 0:
        raise ValueError("Le tableau doit avoir une longueur paire.")

    resultat = []
    for i in range(0, len(tableau), 2):
        paire = f"{tableau[i]} {tableau[i + 1]}"
        resultat.append(paire)

    return resultat
    """

def importJSON(json_as_string):
    importer = JsonImporter()
    return importer.import_(json_as_string)

def rawKialo2Json(kialo_as_string):
    lines = [x for x in kialo_as_string.split("\r\n")]

    # list containing each parsed comment
    result = []

    # we remove the first two lines of the text
    # as we don't need the header
    header = []
    for line in range(0, 6):
        header.append(lines.pop(0))


    subject = header[1]

    lines = group_arguments(lines)


    ##                                            ##
    ##                 REGEDITS                   ##
    ##                                            ##
    # iterate every row in the text file
    for line in lines:

        # find the tree position the comment is in
        tree =  re.search(r"(\d{1,}.)+", line)

        # find if the comment is Pro or Con
        stance = re.search(r"(Con|Pro)(?::)", line)

        # find the text of the comment
        content = re.search(r"((Con|Pro)(?::\s))(.*)", line)

        # define the hierarchy of the current comment
        # which is based on the tree structure

        parsed = re.findall(r"(\d{1,}(?=\.))+", tree.group())
        level = len(parsed)-1

        # make a dictionary with the single entry
        # and put it at the end of the list
        result.append({
            "tree": tree.group(),
            "Level": level,
            "Stance": stance.group(1),
            "ToneInput": content.group(3)
        })
    
    to_write = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

    trees = [x["tree"] for x in result]
    trees = ['1.'] + trees

    resultAsDict = { x["tree"]: x for x in result }

    id2Node = {}

    for idNode in trees:
        
        if idNode == '1.':
            id2Node[idNode] = Node(idNode, subject=subject, tree=idNode)
        else:
            parentId = idNode[:idNode[:-1].rfind(".")+1]
            id2Node[idNode] = Node(
                idNode,
                parent=id2Node[parentId],
                tree=resultAsDict[idNode]["tree"], 
                level=resultAsDict[idNode]["Level"], 
                stance=resultAsDict[idNode]["Stance"], 
                toneInput=resultAsDict[idNode]["ToneInput"].strip(), 
                subject=subject,
                selected=False,
            )


    exporter = JsonExporter(indent=2, sort_keys=True)

    return id2Node['1.']