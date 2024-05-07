import copy
from graphUI.editNode import editNodeUI
from llms.llms import loadModel
import streamlit as st
import time
from io import StringIO
from anytree import Node, RenderTree, PreOrderIter
from anytree.exporter import JsonExporter
from dataProcessing import rawKialo2Json
from graphUI import argumentGraph
from graphUI import argumentAncestor
from streamlit_extras.stylable_container import stylable_container


import streamlit.components.v1 as components
import pandas as pd
import numpy as np

import json

import nest_asyncio
nest_asyncio.apply()


st.set_page_config(layout="wide")


_LOREM_IPSUM = "Please upload a debate file in the left sidebar\n\n"


def stream_data():
    for word in _LOREM_IPSUM:
        yield word
        time.sleep(0.05)



# print("")
# print("")
# print("-----------------------------")
# print("")
# print("")

c1, c2= st.columns((1, 5))

def uploadChanged():
    if st.session_state["uploaded_file"] != None:
        # print("uploadChanged", st.session_state["uploaded_file"])
        stringio = StringIO(st.session_state["uploaded_file"].getvalue().decode("utf-8"))

        extension = st.session_state["uploaded_file"].name.split(".")[1]

        if extension == "txt":
            st.session_state.root = rawKialo2Json.rawKialo2Json(stringio.getvalue())
        elif extension == "json":
            # print("load json anytree")
            st.session_state.root = rawKialo2Json.importJSON(stringio.getvalue())
    else:
        # print("uploadChanged", st.session_state["uploaded_file"])
        st.session_state.root = None
        st.session_state.selection      = {"edges":[], "nodes":[]}
        st.session_state.selection_save      = {"edges":[], "nodes":[]}
def llmChoiceChanged():
    loadModel()

with st.sidebar:

    # st.title("Settings")

    with st.container(border=True): 
        st.markdown("### File")
        st.file_uploader("Import Debate",
                            key="uploaded_file",
                            type=["txt", "json"],
                            accept_multiple_files=False,
                            on_change=uploadChanged
                            )
        
        if 'root' in st.session_state and st.session_state.root != None:
            exporter = JsonExporter(indent=2, sort_keys=True)
            st.download_button("Download the argument tree",
                            data=exporter.export(st.session_state.root),
                            file_name=st.session_state.root.subject.replace(" ","_")+"anytree.json"
                            )
    with st.container(border=True): 
        st.markdown("### Large Language Model")

        if "modelList" not in st.session_state or st.session_state.modelList == None:
            with open("./models.json") as f:
                st.session_state["modelList"] = json.load(f)

        

        st.radio(
            label               = "LLM Choice",
            options             = st.session_state["modelList"],
            key                 = "llm_choice",
            on_change           = llmChoiceChanged,
            label_visibility    = "collapsed",
            format_func         = lambda x : x["display_name"]
        )
        if "llm_model" not in st.session_state or st.session_state.llm_model == None:
            loadModel()

    with st.container(border=True): 
        st.markdown("### Inference technique")

        st.radio(
            label               = "LLM Choice",
            options             = ["0-Shot","Fixed 4-Shots"],
            key                 = "inf_technique",
            label_visibility    = "collapsed",
        )

if 'root' in st.session_state and st.session_state.root != None:

    st.title(st.session_state.root.subject)

    col1, col2 = st.columns([1, 3])

    with stylable_container(key="green_button",css_styles="* { align-items: flex-end;}"):
        with col1:
            with stylable_container(key="col1", css_styles = """
                    .e1f1d6gn0 {
                        //background-color: blue;
                        display: flex;
                        flex-direction: column-reverse;
                    }
                    """):
                with st.container(border=True, height=739) as container:      
                    #If there is a selection
                    if "selection" in st.session_state:
                        # print(st.session_state.selection)
                        if len(st.session_state.selection["nodes"]) + len(st.session_state.selection["edges"]) == 0:
                            st.write("Please select a Node or an Edge")
                        else:
                            if len(st.session_state.selection["nodes"]) > 0:
                                argumentAncestor.argument_ancestors_UI(st.session_state.selection["nodes"][0], st.session_state.root, "")
                            else:
                                st.session_state["inverseEditedColor"] = False
                                #st.write("editNode")
                                editNodeUI(st.session_state.root)
    with col2:
        with st.container(border=True) as container:
            st.session_state["selection"] = argumentGraph.argumentGraph_Cytoscape(st.session_state.root)

            if "selection_save" not in st.session_state:
                #  print("init selection_save")
                 st.session_state.selection_save = st.session_state.selection

            if str(st.session_state.selection) == str({'nodes': [], 'edges': []}) and str(st.session_state.selection_save) != str(st.session_state.selection):
                # print("re init session_state")
                st.session_state["selection"] = st.session_state["selection_save"]

            if str(st.session_state.selection) != str(st.session_state.selection_save) and str(st.session_state.selection) != str({'nodes': [], 'edges': []}):
                st.session_state.selection_save = st.session_state.selection
                if len(st.session_state.selection["nodes"])  > 0 :
                    argumentGraph.colorSelectedNodes(st.session_state.selection["nodes"], st.session_state.root)
                elif len(st.session_state.selection["edges"])  > 0 :
                    argumentGraph.colorSelectedEdge(st.session_state.selection["edges"], st.session_state.root)
                    st.session_state["rootCopy"] = copy.deepcopy(st.session_state.root) 
                st.session_state["selection"] = argumentGraph.argumentGraph_Cytoscape(st.session_state.root)
                st.session_state["selection"] = st.session_state["selection_save"]

else:
    st.session_state["node_selected"] = None
    st.title("Waiting for a debate file")
    st.write_stream(stream_data)


