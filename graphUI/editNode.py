import copy
import anytree
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from anytree import Node, PreOrderIter
import time
import numpy as np
import matplotlib.pyplot as plt

from graphUI.argumentAncestor import argumentUI, editingArgumentUI, findNodeById
from llms.llms import relationsClf, scorePlot


# @st.experimental_fragment
def editNodeUI(root):
    topNodeId = st.session_state.selection["edges"][0].split("-")[0]
    bottomNodeId = st.session_state.selection["edges"][0].split("-")[1]

    topNode     = findNodeById(topNodeId, st.session_state.rootCopy)
    st.session_state["bottomNode"]  = findNodeById(bottomNodeId, st.session_state.rootCopy)


    argumentUI(topNode, displayArrow=False)

    s = {"attack":0.8, "support": 0.2}
    s,prompt = relationsClf(topNode, st.session_state["bottomNode"].toneInput)
    
    if s["attack"] > s["support"]:
        st.session_state["bottomNode"].stance = "Con"
    else:
        st.session_state["bottomNode"].stance = "Pro"

    if st.session_state["bottomNode"].stance == "Con":
        color = 'Tomato'    
    else:        
        color = "LightGreen"



    html_string = """
        <div style="text-align: center;">
        <svg width="64px" height="64px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M7.33199 7.68464C6.94146 8.07517 6.3083 8.07517 5.91777 7.68464C5.52725 7.29412 5.52725 6.66095 5.91777 6.27043L10.5834 1.60483C11.3644 0.823781 12.6308 0.82378 13.4118 1.60483L18.0802 6.27327C18.4707 6.66379 18.4707 7.29696 18.0802 7.68748C17.6897 8.078 17.0565 8.078 16.666 7.68748L13 4.02145V21.9999C13 22.5522 12.5523 22.9999 12 22.9999C11.4477 22.9999 11 22.5522 11 21.9999V4.01666L7.33199 7.68464Z" fill='"""+color+"""'></path> </g></svg>
        </div>
    """
    st.markdown(html_string, unsafe_allow_html=True)
    
    with stylable_container(key="argTextAreaStyle", css_styles="textarea { border:solid ; border-width:thick ; border-color:"+color+" ; background-color:#f5f5f5 ; color:black}"):
        st.session_state["bottomNode"].toneInput = st.text_area(label="machin", value=st.session_state["bottomNode"].toneInput, label_visibility="hidden")

    # switch = st.button("switch", on_click=verify(placeholder))

    fig, ax = scorePlot(s,legend=False)
    st.pyplot(fig)

    col1, col2 = st.columns([0.5,0.5])

    with col1:
        with stylable_container("inferBtn", css_styles="button {width: 100;}"):
            switch = st.button("Infer Relation")

            #if switch:
            #    st.rerun()
    with col2:
        with stylable_container("saveBtn", css_styles="button {width: 100;}"):
            save = st.button("Save Relation")

            if save:
                st.session_state.root = st.session_state.rootCopy