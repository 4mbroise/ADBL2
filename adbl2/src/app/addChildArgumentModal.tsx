import { Box, Button, Grid, Modal, ModalClose, Option, Select, Sheet, Snackbar, Stack, Textarea, Tooltip, Typography } from "@mui/joy";
import { useContext, useEffect, useState } from "react";
import AddIcon from '@mui/icons-material/Add';
import NorthIcon from '@mui/icons-material/North';
import { barOptions, inferRelation, inferenceResultToDataset } from "../utils/inference";
import { AppContext, SnackbarContext } from "./page";
import { Bar } from "react-chartjs-2";
import InfoIcon from '@mui/icons-material/Info';
import { addChild } from "../utils/kialo-parser";
import { predictBinRelation } from "@/service/adbl2-api";


export default function AddChild(props) {
  const [open, setOpen] = useState(false);
  const [childArg, setchildArg] = useState("");
  const [relationType, setRelationType] = useState(undefined);
  const [isInfering, setIsInfering] = useState(false);

  const [confirm, setConfirm] = useState(false);
  const [confirmData, setConfirmData] = useState({ datasets: []});
  const [predictionResult, setPredictionResult] = useState(undefined)

  const { snack, setSnack } = useContext(SnackbarContext);
  const { graph, setGraph, model, promptTechnique } = useContext(AppContext)




  useEffect( () => {
    setchildArg("")
    setRelationType(undefined)
    setConfirm(false)
    setConfirmData({ datasets: []})
    setPredictionResult(undefined)
  }, [])

  const canAdd = () => {
    return childArg !== "" && !!relationType
  }

  const getArgColor = () => {
    console.log("relationTyperelationTyperelationTyperelationType", relationType)
    if(relationType === undefined) {
      return "transparent"
    } else if ( relationType === "Con"){
      return "tomato"
    } else {
      return "lightgreen"
    }
  }

  const infer = () => {
    setIsInfering(true)
    console.log("snack", snack)
    // setSnack({open:true})

    let tmpRelationType = "Con"
    if(relationType === "Con") {
      tmpRelationType = "Pro"
    }

    predictBinRelation(model, props.arg.toneInput, childArg, promptTechnique).then((res) => {

      setConfirm(true)

      console.log("confirmData", inferenceResultToDataset(res))


      let stancePrediction = "Pro"
      if(res.attack > res.support) {
        stancePrediction = "Con"
      }

      // Cas où le type de relation ne match pas la prédiction du modèle
      if(stancePrediction !== relationType) {
        setConfirmData(inferenceResultToDataset(res))
        setPredictionResult(res)
        setConfirm(true)
      } else {
        setGraph(Object.create(addChild(graph, props.arg.id, childArg, relationType)))
        setOpen(false)   
        setIsInfering(false)
      }
    })
  }

  const closeModal = () => {
    if(!confirm) {
      console.log("close")
      setOpen(false)
    }
  }


  return (
    <>
      <Button variant="soft" startDecorator={<AddIcon/>} color="success" onClick={() => setOpen(true)}>
          Add a child argument
      </Button>
      <Modal
        aria-labelledby="modal-title"
        aria-describedby="modal-desc"
        open={open}
        onClose={() => closeModal()}
        sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
      >
        <Sheet
          variant="outlined"
          sx={{
            borderRadius: 'md',
            p: 3,
            boxShadow: 'lg',
            width: "55%"
          }}
        >
          <ModalClose variant="plain" sx={{ m: 1 }} />
          <Typography
            component="h2"
            id="modal-title"
            level="h4"
            textColor="inherit"
            fontWeight="lg"
            mb={1}
          >
            Add a child argument
          </Typography>

          {/* <Typography id="modal-desc" textColor="text.tertiary">
            Make sure to use <code>aria-labelledby</code> on the modal dialog with an
            optional <code>aria-describedby</code> attribute.
          </Typography> */}

          
          <Grid
            container
            direction="column"
            justifyContent="space-evenly"
            alignItems="center"
            gap={2}
          >
            <Box p={1} borderRadius={4} width={"100%"}>
              <Textarea minRows={5} size="lg" value={props.arg.toneInput} disabled/>
            </Box>

            {relationType === undefined &&
              <div className="self-center">
                <NorthIcon 
                  fontSize="large"
                />
              </div>
            }

            {!!relationType &&
              <div className="self-center">
                <NorthIcon 
                  fontSize="large"
                  htmlColor={getArgColor()}
                />
              </div>
            }

            <Box p={1} borderRadius={4} width={"100%"} bgcolor={getArgColor()}>
              <Textarea 
                minRows={5} 
                size="lg" 
                placeholder="Write a child argument …" 
                value={childArg} 
                onChange={e => {setchildArg(e.target.value); canAdd();}}
              />
            </Box>

            
            <Grid
              container
              direction="row"
              justifyContent="space-evenly"
              alignItems="center"
              width={"100%"}
            >
              <Box width={"50%"} padding={1}>
                <Select placeholder="Choose the type of relation" className="w-full" value={relationType} onChange={(e,val) => {setRelationType(val); canAdd();}} >
                  <Option value="Con">Attack</Option>
                  <Option value="Pro">Support</Option>
                </Select>
              </Box> 

              <Box width={"50%"} padding={1}>
                <Button className="w-full" disabled={!canAdd()} loading={isInfering} onClick={() => infer()}>
                  Add
                </Button>
              </Box>
            </Grid>
          </Grid>
          <Snackbar 
            open={confirm} 
            autoHideDuration={2500}
            onClose={() => setConfirm(confirm)}
            anchorOrigin={{vertical:'top', horizontal:'center'}}
            color="danger"
            variant="outlined"
          >

            <Stack
              direction="column"
              justifyContent="flex-start"
              alignItems="flex-start"
              spacing={1}
            >
              <Typography level="title-lg" color="danger">Warning</Typography>
              <Stack 
                direction="row" 
                justifyContent="center"
                alignItems="center"
                gap={1}
              >
                {!!predictionResult &&
                  <>
                    {predictionResult.attack > predictionResult.support &&
                      <>
                        <Typography 
                          color="danger">
                          Your argument has been classified as an attack
                        </Typography>
                        <Tooltip title="Your argument may not be explicit enough to be classified as an attack">
                          <InfoIcon/>
                        </Tooltip> 
                      </>
                    }
                    {predictionResult.attack <= predictionResult.support &&
                      <>
                        <Typography 
                          color="danger">
                          Your argument has been classified as a support
                        </Typography>
                        <Tooltip title="Your argument may not be explicit enough to be classified as a support">
                          <InfoIcon/>
                        </Tooltip> 
                      </>
                    }
                  </>
                }
              </Stack>
              <Bar options={barOptions} data={confirmData}></Bar>
              <Stack direction="row" spacing={1}>
                <Button 
                  variant="solid" 
                  color="danger"
                  onClick={() => {setConfirm(false); setIsInfering(false)}}
                >
                  Reformulate the argument
                </Button>
                <Button
                  variant="outlined"
                  color="danger"
                  onClick={() => {setGraph(Object.create(addChild(graph, props.arg.id, childArg, relationType))); setOpen(false)}}
                >
                  {!!predictionResult && predictionResult.attack > predictionResult.support &&
                    <>
                      Add it as a support
                    </>
                  }
                  {!!predictionResult && predictionResult.attack <= predictionResult.support &&
                    <>
                      Add it as an attack
                    </>
                  }
                </Button>
              </Stack>
            </Stack>

          </Snackbar>
        </Sheet>
      </Modal>
    </>
  );
}