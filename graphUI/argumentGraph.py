from streamlit_agraph import agraph, Node, Edge, Config
import anytree
from st_cytoscape import cytoscape
import streamlit as st

from graphUI.argumentAncestor import getNodeAncestors
import time


def colorSelectedNodes(selectedIdNodes, anytreeRoot):
  # print("selectedIdNodes", selectedIdNodes)
  for node in anytree.PreOrderIter(anytreeRoot):
    if node.tree in selectedIdNodes:
      for ancestor in getNodeAncestors(node):
        ancestor.selected = True
    else:
      node.selected = False

def colorSelectedEdge(selectedIdEdge, anytreeRoot):
  nodeIds = selectedIdEdge[0].split("-")
  for node in anytree.PreOrderIter(anytreeRoot):
    if node.tree in nodeIds:
        node.selected = True
    else:
      node.selected = False


def argumentGraph(anytreeRoot: anytree.Node):


  agraphNodes = []
  agraphEdges = []

  for node in anytree.PreOrderIter(anytreeRoot):

    # not root node case
    if node.name != "1.":  
      agraphNodes.append(Node(id=node.tree,
                              stance=node.stance,
                              toneInput=node.toneInput,
                              tree=node.tree))
      agraphEdges.append(Edge(source=node.tree, target=node.parent.tree))
    #root node case
    else:
      agraphNodes.append(Node(id=node.tree,
                              subject=node.subject,
                              tree=node.tree,size=100))

      """for i in range(100):
        agraphEdges.append(Edge(source=node.tree, target=node.tree))"""

    config = Config(width=750,
                height=950,
                directed=True, 
                physics=False, 
                hierarchical=True,

                shakeTowards="leaves"
                # **kwargs
                )

  return agraph(nodes=agraphNodes, edges=agraphEdges, config=config)



def argumentGraph_Cytoscape(anytreeRoot: anytree.Node):

  elements = []

  nodes = [x for x in anytree.PreOrderIter(anytreeRoot)]

  selection = [x for x in nodes if x.name != "1." and x.selected]

  for node in nodes:
    # not root node case
    if node.name != "1.":

      color = None


      if len(selection) <= 0:
        if node.stance == "Con":
          color = 'Tomato'
        else:
          color = 'LightGreen'
      else:
        if node.selected:
          if node.stance == "Con":
            color = '#b31b00'
          else:
            color = '#189a18'    
        else:
          if node.stance == "Con":
            color = "#ffbeb3"
          else:
            color = '#90ee90'

      # add node
      elements.append({
        "data": {
          "id"        : node.tree,
          "stance"    : node.stance,
          "toneInput" : node.toneInput,
          "tree"      : node.tree,
          "color"     : color,
          "selected"  : "purple"
        }
      })

      if "selection" in st.session_state and len(st.session_state.selection["edges"]) != 0 and st.session_state["selection"]["edges"][0] == node.parent.tree+"-"+node.tree:
        # print("color", node.parent.tree+"-"+node.tree)
        if node.stance == "Con":
          elements.append({
            "data": {
                "source"    : node.tree, 
                "target"    : node.parent.tree, 
                "id"        : (node.parent.tree+"-"+node.tree).replace(" ","_"),
                "color"     : '#b31b00',
              }
            })
        else:
          elements.append({
            "data": {
                "source"    : node.tree, 
                "target"    : node.parent.tree, 
                "id"        : (node.parent.tree+"-"+node.tree).replace(" ","_"),
                "color"     : '#189a18',
              }
            })
      else:
        if "selection" in st.session_state and len(st.session_state.selection["edges"]) > 0:
          if node.stance == "Con":
            color = '#b31b00'
          else:
            color = '#189a18' 
          if node.stance == "Con":
            color = "#ffbeb3"
          else:
            color = '#90ee90'
      
        # add edgex 
        elements.append({
          "data": {
              "source"    : node.tree, 
              "target"    : node.parent.tree, 
              "id"        : (node.parent.tree+"-"+node.tree).replace(" ","_"),
              "color"     : color,
            }
          })

    #root node case
    else:
      # add root node
      elements.append({
        "data": {
          "id"        : node.tree,
          "subject"   : node.subject,
          "color"     : "dodgerblue",
          
        }
      })

  stylesheet = [
    {
      "selector": "node", 
      "style": {
        "width": 20, 
        "height": 20,
        "background-color": "data(color)",
        "height"    : 25,
        "width"    : 25
      }
    },
    {
      "selector": "edge", 
      "style": {
        "line-color": "data(color)",
      }
    },
    {
        "selector": ":selected",
        "style": {
          "overlay-color":"teal",
          "overlay-opacity":1,
          "overlay-shape":"ellipse",
          "overlay-padding":0
        },
    },

  ]



  return cytoscape(elements,
                   stylesheet, 
                   key=None, 
                   height="700px", 
                   layout={
                      "name"            : "breadthfirst",
                      "roots"           : ["1."],
                      "animate"         : True,
                      "spacingFactor"   : 3,
                      "fit"             : True
                    },
                   selection_type="single",
                   )
                   