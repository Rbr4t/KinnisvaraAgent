import Navbar from "../components/Navbar";
import {
  CssBaseline,
  Container,
  Grid,
  Paper,
  TextField,
  Typography,
  Button,
  List,
  Switch,
  ListItem,
  Box,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  AccordionActions,
  Checkbox,
} from "@mui/material";
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import Tooltip from "@mui/material/Tooltip";

import ExpandMoreIcon from "@mui/icons-material/ExpandMoreRounded";
import { useEffect, useState } from "react";
import Select from "../components/Dropdown";
import data from "../assets/output.json";

const label = { inputProps: { "aria-label": "Checkbox demo" } };

async function isLoggedIn() {
  const response = await fetch("/auth/get_user_info", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${sessionStorage.getItem("access_token")}`,
    },
  });

  if (!response.ok) {
    return false;
  }

  return true;
}

export default function Dashboard() {
  const [location, setLocation] = useState("");
  const [price, setPrice] = useState("");
  const [area, setArea] = useState("");
  const [rooms, setRooms] = useState("");
  const [lisaParameetrid, setLisaParameetrid] = useState({
    uued: false,
    varieerumine: false,
  });
  const [queries, setQueries] = useState([]);
  const handleAddQuery = () => {
    setQueries([
      ...queries,
      {
        location,
        price,
        area,
        rooms,
        lisaParameetrid,
        date: new Date().toLocaleString(),
      },
    ]);
    console.log({
      price: parseFloat(price),
      area: parseFloat(area),
      rooms: parseInt(rooms),
      date: new Date().toLocaleString(),
      token: sessionStorage.getItem("access_token"),
      location: location,
    });
    setLocation("");
    setPrice("");
    setArea("");
    setRooms("");
    setSelectedAddress([]);
    setLisaParameetrid({
      uued: false,
      varieerumine: false,
    });
    console.log(
      JSON.stringify({
        price: parseFloat(price),
        area: parseFloat(area),
        rooms: parseInt(rooms),
        date: new Date().toLocaleString(),
        token: sessionStorage.getItem("access_token"),
        location: location,
      })
    );
    const sendReq = async () => {
      const response = await fetch("/api/add_search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          price: parseFloat(price),
          area: parseFloat(area),
          rooms: parseInt(rooms),
          token: sessionStorage.getItem("access_token"),
          location: location,
        }),
      });
      if (response.ok) {
        return true;
      } else {
        return false;
      }
    };
    sendReq();
  };

  useEffect(() => {
    const reqQueries = async () => {
      const token = sessionStorage.getItem("access_token");
      console.log(JSON.stringify({ token }));

      try {
        const resp = await fetch("/api/get_searches", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ token }),
        });

        console.log(resp.status);

        if (!resp.ok) {
          throw new Error(`HTTP error! status: ${resp.status}`);
        }

        const userData = await resp.json();
        setQueries(userData.searches);
      } catch (error) {
        console.error("There was an error!", error);
      }
    };

    reqQueries();
  }, []); // The empty array ensures this effect runs only once

  const [selectedAddress, setSelectedAddress] = useState([]);

  const handleSelectChange = (index, value) => {
    let newSelectedAddress = [...selectedAddress];
    newSelectedAddress[index] = value;

    if (value === null) {
      newSelectedAddress = newSelectedAddress.slice(0, index);
    }
    console.log(newSelectedAddress);
    setLocation(newSelectedAddress.join(", "));
    setSelectedAddress(newSelectedAddress);
  };

  async function checkLogin() {
    if (!(await isLoggedIn())) {
      window.location.href = "/login";
      return <></>;
    }
  }
  checkLogin();

  return (
    <>
      <CssBaseline />
      <Navbar />
      <Container>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ padding: 2 }}>
              <Typography variant="h6" gutterBottom>
                Parameetrid
              </Typography>
              <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
                <Box>
                  <Typography variant="h8" gutterBottom>
                    Aadress
                  </Typography>
                  <Select
                    clear={queries}
                    onAsukohtChange={(value) => {
                      handleSelectChange(0, value);
                      console.log(selectedAddress[0]);
                    }}
                    kohad={Object.keys(data)}
                  />
                  {selectedAddress.length >= 1 ? (
                    <Select
                      disabled={selectedAddress.length < 1}
                      onAsukohtChange={(value) => {
                        handleSelectChange(1, value);
                      }}
                      kohad={Object.keys(data[selectedAddress[0]] || {})}
                    />
                  ) : null}

                  {selectedAddress.length >= 2 ? (
                    <Select
                      onAsukohtChange={(value) => {
                        handleSelectChange(2, value);
                      }}
                      kohad={Object.keys(
                        data[selectedAddress[0]][selectedAddress[1]] || {}
                      )}
                    />
                  ) : null}
                  {selectedAddress.length >= 3 &&
                  data[selectedAddress[0]][selectedAddress[1]][
                    selectedAddress[2]
                  ].length > 0 ? (
                    <Select
                      onAsukohtChange={(value) => {
                        handleSelectChange(3, value);
                      }}
                      kohad={
                        data[selectedAddress[0]][selectedAddress[1]][
                          selectedAddress[2]
                        ] || []
                      }
                    />
                  ) : null}
                </Box>

                <TextField
                  label="Hind"
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                  fullWidth
                />
                <TextField
                  label="Pindala (m2)"
                  value={area}
                  onChange={(e) => setArea(e.target.value)}
                  fullWidth
                />
                <TextField
                  label="Ruumide arv"
                  value={rooms}
                  onChange={(e) => setRooms(e.target.value)}
                  fullWidth
                />
                <FormControl component="fieldset">
                  <FormLabel component="legend">Lisaparameetrid</FormLabel>
                  <FormGroup aria-label="position" row>
                    <Tooltip title="alates tänasest">
                      <FormControlLabel
                        checked={lisaParameetrid.uued}
                        onChange={(event) =>
                          setLisaParameetrid((prevState) => ({
                            ...prevState,
                            uued: event.target.checked,
                          }))
                        }
                        value="start"
                        control={<Checkbox />}
                        label="Ainult uued kuulutused"
                        labelPlacement="start"
                      />
                    </Tooltip>
                    <FormControlLabel
                      checked={lisaParameetrid.varieerumine}
                      onChange={(event) =>
                        setLisaParameetrid((prevState) => ({
                          ...prevState,
                          varieerumine: event.target.checked,
                        }))
                      }
                      value="start"
                      control={<Checkbox />}
                      label="Parameetrite varieerumisruum"
                      labelPlacement="start"
                    />
                  </FormGroup>
                </FormControl>
                <Button variant="contained" onClick={handleAddQuery}>
                  Lisa otsing
                </Button>
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ padding: 2 }}>
              <Typography variant="h6" gutterBottom>
                Aktiivsed otsingud
              </Typography>
              <List>
                {queries.map((query, index) => (
                  <Accordion key={index}>
                    <AccordionSummary
                      expandIcon={<ExpandMoreIcon />}
                      aria-controls="panel1-content"
                      id="panel1-header"
                    >
                      {query.location}
                    </AccordionSummary>
                    <AccordionDetails>
                      <List>
                        <ListItem>Max Hind: {query.price}</ListItem>
                        <ListItem>Pindala: {query.area}</ListItem>
                        <ListItem>Ruume: {query.rooms}</ListItem>
                      </List>
                    </AccordionDetails>
                    <AccordionActions>
                      Aktiivne {query.date} saadik
                      <Switch>Active/not</Switch>
                    </AccordionActions>
                  </Accordion>
                ))}
              </List>
            </Paper>
          </Grid>

          <Grid item xs={12} md={12}>
            <Paper elevation={3} sx={{ padding: 2 }}>
              <Typography variant="h6" gutterBottom>
                Leitud korterid
              </Typography>
              <List>
                <Accordion>
                  <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel1-content"
                    id="panel1-header"
                  >
                    {}
                  </AccordionSummary>
                  <AccordionDetails>
                    <List>
                      <ListItem>Price: {}</ListItem>
                      <ListItem>Area: {}</ListItem>
                      <ListItem>Rooms: {}</ListItem>
                    </List>
                  </AccordionDetails>
                  <AccordionActions>
                    Aktiivne {} saadik
                    <Switch>Active/not</Switch>
                  </AccordionActions>
                </Accordion>
              </List>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </>
  );
}
