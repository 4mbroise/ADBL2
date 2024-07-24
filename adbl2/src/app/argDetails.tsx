import Close from "@mui/icons-material/Close"
import { Box, Button, CircularProgress, Grid, IconButton, LinearProgress, Skeleton, Snackbar, Textarea, Typography } from "@mui/joy"
import Grid2 from "@mui/material/Unstable_Grid2"
import { useContext, useEffect, useRef, useState } from "react"
import NorthIcon from '@mui/icons-material/North';
import { Bar } from "react-chartjs-2";
import RefreshIcon from '@mui/icons-material/Refresh';
import AddIcon from '@mui/icons-material/Add';
import SaveIcon from '@mui/icons-material/Save';
import CloseIcon from '@mui/icons-material/Close';
import DeleteIcon from '@mui/icons-material/Delete';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import AddChild from "./addChildArgumentModal";
import { AppContext } from "./page";
import { inferRelation, inferenceResultToDataset } from "../utils/inference";
import { predictBinRelation } from "@/service/adbl2-api";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function ArgumentDetailsUI(props) {

  const [ isVisible, setVisible ] = useState(true)
  const [ isAddSuccess, setIsAddSuccess ] = useState(false)
  const [ isInfering, setIsInfering ] = useState(true)
  const [ arg, setArg ] = useState(props.bottomArg.toneInput)
  const [inferenceData, setInferenceData] = useState({ datasets: []});
  const [inferenceResult, setInferenceResult]  = useState(undefined)
  const { graph, setGraph, model, promptTechnique } = useContext(AppContext)


  useEffect(() => {

    setArg(props.bottomArg.toneInput)

    setIsAddSuccess(false)

    setIsInfering(true)
    if(!!props.topArg){

      predictBinRelation(model, props.topArg.toneInput, props.bottomArg.toneInput, promptTechnique).then((res) => {
        setInferenceData(inferenceResultToDataset(res))
        setIsInfering(false)
      })

      //inferRelation().then(() => setIsInfering(false))
    } else {
      setIsInfering(false)
    }    
  }, [props.topArg, props.bottomArg])

  const ref1 = useRef(null);
  const ref2 = useRef(null);
  
  const handleOutSideClick = (event) => {
    if (!ref1.current?.contains(event.target)) {
      props.close(undefined)
    }
  };

  const infer = () => {
    setIsInfering(true)
    predictBinRelation(model, props.topArg.toneInput, arg, promptTechnique).then((res) => {
      setInferenceData(inferenceResultToDataset(res))
      setIsInfering(false)
    })
  }

  const style1 = { 
    top:props.posY,
    left: props.posX,
    width: '30%',
    visibility: "visible",
    borderRadius: 10
  }

  const style2 = { 
    backgroundColor:"#d3d3d3"
  }

  let topArgColor = "#d3d3d3"
  let topArgBorderColor = "#d3d3d3"
  if(!!props.topArg) {
    if(props.topArg.stance === "Pro") {
      topArgColor = "#a7f1a7"
      topArgBorderColor = "#1cb01c"
    } else if (props.topArg.stance === "Con") {
      topArgColor = "#ffa899"
      topArgBorderColor = "#cc1f00"
    } else if (props.topArg.stance === "Root") {
      topArgColor = "#80bfff"
      topArgBorderColor = "#0066cc"
    }  
  }


  let bottomArgColor = "#d3d3d3"
  let bottomBorderArgColor = "#d3d3d3"
  if(props.bottomArg.stance === "Pro") {
    bottomArgColor = "#a7f1a7"
    bottomBorderArgColor = "#0a420a"
  } else if (props.bottomArg.stance === "Con") {
    bottomArgColor = "#ffa899"
    bottomBorderArgColor = "#4d0b00"
  } else if (props.bottomArg.stance === "Root") {
    bottomArgColor = "#80bfff"
    bottomBorderArgColor = "#00264d"
  }


  const save = () => {

    var n = graph.first( (node) => {
      return node.model.id === props.bottomArg.id;
    });

    n.model.toneInput = arg
    setGraph(Object.create(graph))
  }


  const labels = ['mmhm'];
  const tmpPercent = Math.floor(Math.random() * 100)
  
  const tmpData = {
    labels,
    datasets: [
      {
        label: 'Attack',
        data: [tmpPercent],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: '#ff9380',
      },
      {
        label: 'Support',
        data: [100-tmpPercent],
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: '#bfff80',
      },
    ],
  }
  const options = {
    maintainAspectRatio: false,
    indexAxis: 'y' as const,
    plugins: {
      title: {
        display: false,
      },
      tooltip: {
        callbacks: {
           title : () => null
        }
     }
    },
    responsive: true,
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
        ticks: {
          display: false
        }
      },
    },
  };


  return (
    <Box className="absolute bg-white" style={style1} ref={ref1} border={2}>
        <Grid
          container
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <div className="invisible">
            <IconButton onClick={()=>props.close(undefined)}>
              <Close/>
            </IconButton>
          </div>
          <Typography
            component="h2"
            id="modal-title"
            level="h4"
            textColor="inherit"
            fontWeight="lg"
            mb={1}
          >
            Argument Details
          </Typography>
          <div>
            <IconButton onClick={()=>props.close(undefined)}>
              <Close/>
            </IconButton>
          </div>
        </Grid>
        <Box className=" w-full h-full rounded-xl" overflow={"auto"} padding={2} paddingTop={2}/* style={style2} */ >
          <Grid container
                direction="column"
                justifyContent="center"
                gap={3}
          >  
            {!!props.topArg &&
              <>
                <Box bgcolor={topArgColor} p={1} borderRadius={4} /* border={2} borderColor={topArgBorderColor} */>
                  <Textarea size="lg" name="Size" value={props.topArg.toneInput} key={props.topArg.toneInput} className="pointer-events-none"/>
                </Box>
                <div className="self-center">
                  <NorthIcon fontSize="large" htmlColor={bottomArgColor}/>
                </div>
              </>
            }

            {!props.topArg &&
              <Box bgcolor={bottomArgColor} p={1} borderRadius={4} border={3} borderColor={bottomBorderArgColor}>
                <Textarea size="lg" name="Size" value={arg} key={props.bottomArg.toneInput} onChange={e => setArg(e.target.value)} className="pointer-events-none"/>
              </Box>
            }

            {!!props.topArg &&
              <div>
                <Box bgcolor={bottomArgColor} p={1} borderRadius={4} border={3} borderColor={bottomBorderArgColor}>
                  <Textarea size="lg" name="Size" value={arg} key={props.bottomArg.toneInput} onChange={e => setArg(e.target.value)} />
                </Box>
              </div>
            }

            { !!props.topArg &&
              <Box width={"100%"} className="h-32 relative justify-center">
                { isInfering &&
                  <div className="absolute h-32 w-full flex align-middle">
                    <Skeleton></Skeleton>
                  </div>
                }
                
                { !isInfering &&
                  <Grid
                    container
                    direction="row"
                    alignItems="center"
                    justifyContent="center"
                    className="h-32 content-center"
                  >
                    {/* <Grid item xs={6} className="absolute h-32 flex justify-center">
                      <Bar options={options} data={tmpData} className="absolute m-0" />
                    </Grid> */}
                    <Grid item xs={9}>
                      <Bar options={options} data={inferenceData} />
                    </Grid>
                    <Grid item xs={3} textAlign="center">
                      <Button onClick={() => infer()}
                        variant="plain"
                        size="lg"
                        style={{"border-radius": "99999px"}}
                      >
                        <RefreshIcon fontSize="large"/>
                      </Button>
                    </Grid>
                  </Grid> 
                }
              </Box>
            }
            <AddChild arg={props.bottomArg} graph={props.graph} setGraph={props.setGraph}/>
            <Grid container direction="row" >
              <Grid item xs={6} paddingRight={0.5}>
                <Button variant="solid" startDecorator={<DeleteIcon/>} color="danger" className="w-full">
                  Delete
                </Button>
              </Grid>
              <Grid item xs={6} paddingLeft={0.5}>
                <Button variant="solid" 
                  startDecorator={<SaveIcon/>} 
                  color="primary" 
                  className="w-full" 
                  onClick={save}>
                  Save
                </Button>
              </Grid>
            </Grid>
          </Grid>
          <Snackbar
            autoHideDuration={4000}
            open={isAddSuccess}
            onClose={(event, reason) => {
              if (reason === 'clickaway') {
                return;
              }
              setIsAddSuccess(false);
            }}
          >
          </Snackbar>
        </Box>
    </Box>

  )
}