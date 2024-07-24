import TreeModel from "tree-model";
import { Argument } from "../types/argument";

export function kialoParser(kialoText: string) {
  let lines
  lines = kialoText.split("\r\n").filter((x)=>x !=="").map((x) => x.trim())

  const discussionAndThesis = lines.slice(0, 4);
  lines = lines.slice(4, lines.length)

  
  lines = lines.map((x) => x.replace("Pro:","Pro"))
  lines = lines.map((x) => x.replace("Con:","Con"))

  // Removing sources (lines at the end of kialo files)
  lines = lines.slice(0,lines.indexOf("Sources:"))


  const tmp = []

  for (let index = 0; index < lines.length; index+=2) {
    const element1 = lines[index].split(" ");
    const element2 = lines[index+1];

    tmp.push([element1[0], element1[1], element2])
  }

  lines = tmp

  // console.log("Discussion And Thesis", discussionAndThesis)

  const question = discussionAndThesis[1]



  const tree = new TreeModel()
  
  const rootTmp: Argument = {
    id:         "1.",
    stance:     "Root",
    toneInput:  discussionAndThesis[3],
    question: question
  } 
  
  const root = tree.parse(rootTmp)


  for (let index = 0; index < lines.length; index++) {
    const id        = lines[index][0];
    const stance    = lines[index][1];
    const toneInput = lines[index][2];

    const parentId = id.slice(0, id.slice(0,id.length-1).lastIndexOf(".")+1)


    const parent = root.first(x => x.model.id === parentId)
    if ( parent !== undefined) {
      
      const arg = {
        id:         id,
        stance:     stance,
        toneInput:  toneInput,
        question: question
      } as Argument
   
      parent.addChild(tree.parse(arg))
    } else {
      console.log("")
    }
  }
  return root
}

export function addChild(root, parentId, childArgument, stance) {

  const tree = new TreeModel()

  const parentNode = root.first( (x) => x.model.id === parentId)
  const nextId = getNextId(parentNode)

  const newArgument: Argument = {
    id:         nextId,
    stance:     stance,
    toneInput:  childArgument
  }

  parentNode.addChild(tree.parse(newArgument))

  return root
}

function getNextId(parentNode) {

  const children = parentNode.children

  let nextSubId = 1

  if(children.length !== 0) {
    nextSubId = Math.max(...children.map(x => {
      const tmp = x.model.id.slice(0,x.model.id.length - 1).split(".")
      return Number(tmp[tmp.length -1])
    })) + 1
  }
  const nextId = parentNode.model.id + nextSubId + "."

  console.log(nextId)
  return nextId
}