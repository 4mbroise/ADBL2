import TreeModel from "tree-model";
import { Argument } from "../types/argument";

export function jsonParser(jsonGraph: string) {

  console.log("jsonGraph", JSON.parse(jsonGraph))
  const tree = new TreeModel()
  const root = tree.parse(JSON.parse(jsonGraph));

  return root
}