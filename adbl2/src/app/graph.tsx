import { useContext, useMemo, useState } from "react";
import { AppContext } from "./page";
import CytoscapeComponent from 'react-cytoscapejs';
import cytoscape from "cytoscape";
import elk from 'cytoscape-elk';
import ArgumentDetailsUI from "./argDetails";
import { Typography } from "@mui/joy";

cytoscape.use(elk)




export default function GraphUI(props) {

  const { graph, setGraph }                                   = useContext(AppContext)
  const [ cy, setCy ]                                         = useState(undefined)
  const [ selectedNode, setSelectedNode ]                     = useState(undefined)
  const [ selectedParentNode, setSelectedParentNode ]         = useState(undefined)
  const [ pos, setPos ]                                       = useState(undefined)

  const cytoscapeData: any[] = []

  const memoGraph = useMemo(() => {
    return <CytoscapeComponent 
    elements={props.data}
    className="flex-auto"
    cy={(cy) => setCy(cy)}
    layout= { 
      {
        name : 'elk',
        elk: {
          'elk.direction': 'UP',
        }
      }
    }
  />
  }, [props.data]);



  if(!!cy) {
    cy.on("mouseover", "node", (event) => {
      event.preventDefault();
      setPos({x:event.originalEvent.x, y:event.originalEvent.y})
      setSelectedNode(event.target._private.data)

      // cy.nodes().style("border-style", "solid")
      // cy.nodes().style("border-width", 0)

      event.target.style("border-style", "solid")
      event.target.style("border-width", 5)

      if(event.target._private.data.id !== "1.") {

        event.target.style("border-style", "solid")
        event.target.style("border-width", 5)

        const parentId = cy.edges('[source="'+event.target._private.data.id+'"]')[0]._private.data.target
        const parentNode = cy.nodes('[id="'+parentId+'"]')[0]._private.data
        setSelectedParentNode(parentNode)
      } else {
        setSelectedParentNode(undefined)
      }
    })

    cy.on("mouseout", "node",(event) => {
      var evtTarget = event.target;
      event.preventDefault();
      event.target.style("border-width", 0)
    })

    cy.on("click", (event) => {
      var evtTarget = event.target;
      event.preventDefault();
    
      if( evtTarget === cy ){
        setSelectedNode(undefined)
      }   
    })

    cy.nodes('[stance="Con"]').style('background-color', 'Tomato');
    cy.nodes('[stance="Root"]').style('background-color', 'DodgerBlue');
    cy.nodes('[stance="Pro"]').style('background-color', 'LightGreen');

    cy.nodes().map(x => x._private.data).forEach(node => {
      if(node.stance !== 'Root'){
        if(node.stance === "Con") {
          cy.edges('[source="'+node.id+'"]').style('lineColor', 'Tomato');
        }
        if(node.stance === "Pro") {
          cy.edges('[source="'+node.id+'"]').style('lineColor', 'LightGreen');
        }
      }
    });

  }


  
  return (
    <>
      <Typography
            component="h2"
            id="modal-title"
            level="h1"
            textColor="inherit"
            fontWeight="lg"
            mb={1}
            className="relative"
      >
        {props.graph.model.question}
      </Typography>
      { memoGraph }
      {
        !!selectedNode &&
        <ArgumentDetailsUI bottomArg={selectedNode} topArg={selectedParentNode} posX={pos.x} posY={pos.y} close={setSelectedNode} graph={props.graph} setGraph={props.setGraph} key={selectedNode} />
      }
    </>    
  )
}