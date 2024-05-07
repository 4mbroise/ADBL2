import anytree
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from anytree import Node, PreOrderIter
import time
import numpy as np
import matplotlib.pyplot as plt

from llms.llms import relationsClf, scorePlot


def findNodeById(node_id, tree_root):
  return anytree.search.find(tree_root, lambda x: x.tree == node_id)

def getNodeAncestors(node):
  if node.parent != None:
    return getNodeAncestors(node.parent) + [node]
  else:
    return [node]

def argumentUI(node,modal=None, displayArrow=True):
  if node.tree != '1.':
    if node.stance == "Con":
      html_string = """
        <div style="text-align: center;">
          <svg width="64px" height="64px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M7.33199 7.68464C6.94146 8.07517 6.3083 8.07517 5.91777 7.68464C5.52725 7.29412 5.52725 6.66095 5.91777 6.27043L10.5834 1.60483C11.3644 0.823781 12.6308 0.82378 13.4118 1.60483L18.0802 6.27327C18.4707 6.66379 18.4707 7.29696 18.0802 7.68748C17.6897 8.078 17.0565 8.078 16.666 7.68748L13 4.02145V21.9999C13 22.5522 12.5523 22.9999 12 22.9999C11.4477 22.9999 11 22.5522 11 21.9999V4.01666L7.33199 7.68464Z" fill="Tomato"></path> </g></svg>
        </div>
      """
    else:
      html_string = """
      <div style="text-align: center;">
        <svg width="64px" height="64px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M7.33199 7.68464C6.94146 8.07517 6.3083 8.07517 5.91777 7.68464C5.52725 7.29412 5.52725 6.66095 5.91777 6.27043L10.5834 1.60483C11.3644 0.823781 12.6308 0.82378 13.4118 1.60483L18.0802 6.27327C18.4707 6.66379 18.4707 7.29696 18.0802 7.68748C17.6897 8.078 17.0565 8.078 16.666 7.68748L13 4.02145V21.9999C13 22.5522 12.5523 22.9999 12 22.9999C11.4477 22.9999 11 22.5522 11 21.9999V4.01666L7.33199 7.68464Z" fill="Lightgreen"></path> </g></svg>
      </div>
    """
    if displayArrow:
      st.markdown(html_string, unsafe_allow_html=True)
    
    if node.stance == 'Pro':
      with stylable_container(key="pros",css_styles="* { background-color: lightgreen;}"):
        with st.container(border=True):
          st.write(node.toneInput)
          if modal != None:
            with stylable_container(key="devlop_button_pros",css_styles="* { border-color: black; border-width: thin; width:100%}"):
              open_modal = st.button("Develop", key="dev_arg_"+node.tree)
              if open_modal:
                  developArg(node)

    else:
      with stylable_container(key="cons",css_styles="* { background-color: tomato;}"):
        with st.container(border=True):
          with stylable_container(key="whiteText",css_styles="{ color: white;}"):
            st.write(node.toneInput)
            if modal != None:
              with stylable_container(key="devlop_button_cons",css_styles="* { border-color: white; border-width: thin; width:100%}"):
                open_modal = st.button("Develop", key="dev_arg_"+node.tree)
                if open_modal:
                    developArg(node)
  else:
    with stylable_container(key="subj",css_styles="{ background-color: dodgerblue;}"):
        with st.container(border=True):
          with stylable_container(key="whiteText",css_styles="* { color: white;}"):
            st.write(node.subject)

@st.experimental_fragment
def editingArgumentUI(node, modal=None, displayArrow=True, inverse=False):
  # st.write("test")

  test = stylable_container(key="nn", css_styles="")
  with test:
    if node.tree != '1.':
      if node.stance == "Con":
        color = 'Tomato'
      else:
        color = 'Lightgreen'

      if inverse and color=='Lightgreen':
        color = 'Tomato'
      if inverse and color=='Tomato':
        color = 'Lightgreen'
    
    
    if node.tree != '1.':
      
      html_string = """
        <div style="text-align: center;">
          <svg width="64px" height="64px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M7.33199 7.68464C6.94146 8.07517 6.3083 8.07517 5.91777 7.68464C5.52725 7.29412 5.52725 6.66095 5.91777 6.27043L10.5834 1.60483C11.3644 0.823781 12.6308 0.82378 13.4118 1.60483L18.0802 6.27327C18.4707 6.66379 18.4707 7.29696 18.0802 7.68748C17.6897 8.078 17.0565 8.078 16.666 7.68748L13 4.02145V21.9999C13 22.5522 12.5523 22.9999 12 22.9999C11.4477 22.9999 11 22.5522 11 21.9999V4.01666L7.33199 7.68464Z" fill='"""+color+"""'></path> </g></svg>
        </div>
      """
        
      if displayArrow:
        st.markdown(html_string, unsafe_allow_html=True)

      if "argEdited" in st.session_state:
        del st.session_state["argEdited"]

      key = str(time.time())
      
      with stylable_container(key="ConsWhiteText",css_styles="textarea { border:solid ; border-width:thick ; border-color:"+color+" ; background-color:#f5f5f5 ; color:black}"):
        st.session_state["argEdited"] = st.text_area("Edit",value=node.toneInput, label_visibility="hidden", height=263, key=key)
        # st.text_area("Edit",value=node.toneInput, label_visibility="hidden", height=263, key="argEdited" )


    else:
      with stylable_container(key="subj",css_styles="{ background-color: dodgerblue;}"):
          with st.container(border=True):
            with stylable_container(key="whiteText",css_styles="* { color: white;}"):
              st.write(node.subject)
  return test

@st.experimental_fragment
@st.experimental_dialog("Develop an argument")
def developArg(node):
  with st.container(height=700, border=False):
      with stylable_container(key="argAncestorsInModal", css_styles = """
                    .e1f1d6gn0 {
                        display: flex;
                        flex-direction: column-reverse;
                    }
        """):
        with st.container(height=300, border=True):
            argument_ancestors_UI(node.tree, st.session_state.root)

        html_string = """
          <div style="text-align: center;">
            <svg width="64px" height="64px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M7.33199 7.68464C6.94146 8.07517 6.3083 8.07517 5.91777 7.68464C5.52725 7.29412 5.52725 6.66095 5.91777 6.27043L10.5834 1.60483C11.3644 0.823781 12.6308 0.82378 13.4118 1.60483L18.0802 6.27327C18.4707 6.66379 18.4707 7.29696 18.0802 7.68748C17.6897 8.078 17.0565 8.078 16.666 7.68748L13 4.02145V21.9999C13 22.5522 12.5523 22.9999 12 22.9999C11.4477 22.9999 11 22.5522 11 21.9999V4.01666L7.33199 7.68464Z" fill="#31333f"></path> </g></svg>
          </div>
        """
        st.markdown(html_string, unsafe_allow_html=True)
        newArgument = st.text_area(label="Add a child argument", key="textArea"  )  

        # -------------------------------------
        button1 = st.button('Infer Argument Relation')

        if st.session_state.get('button') != True:

            st.session_state['button'] = button1

        if st.session_state['button'] == True:
            with st.spinner('Wait for it...'):
                score, prompt = relationsClf(node, newArgument)
                fig, ax = scorePlot(score)
                st.pyplot(fig)

                if score["attack"] > score["support"]:
                  st.error("Your argument has been classified as an attack")
                else:
                  st.success("Your argument has been classified as a support")

                with st.expander("See Prompt"):
                  st.text(prompt)

            if st.button('Save Argument'):
                print("Save")

                st.write("Hello, it's working")

                st.session_state['button'] = False

                st.checkbox('Reload')

                if score["attack"] > score["support"]:
                  relation = "Con"
                else:
                  relation = "Pro"

                childsLasNb = [int(x.tree.split(".")[-2]) for x in findNodeById(node.tree, st.session_state.root).children]

                if len(childsLasNb) == 0:
                  childId = node.tree+'1.'
                else:
                  childId = node.tree + str(max(childsLasNb) + 1) +"."

                n = Node("test",
                        parent=findNodeById(node.tree, st.session_state.root),
                        tree=childId,
                        stance=relation,
                        toneInput=newArgument,
                        selected=False)

                st.rerun()
                  
    
def argument_ancestors_UI(node_id, tree_root, modal=None):
  currentNode = findNodeById(node_id, tree_root)

  ancestors = getNodeAncestors(currentNode)

  if modal != None:
    for node in ancestors[:-1]:
      argumentUI(node, modal=modal)      
    with stylable_container(key="selectedArg",css_styles="* { border-width: thick; border-color: teal}"):
      argumentUI(ancestors[-1], modal=modal)
  else:
    for node in ancestors:
      argumentUI(node)