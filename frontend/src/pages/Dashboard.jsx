import Navbar from "../components/Navbar";
import { AccordionActions, CssBaseline } from "@mui/material";
import React, { useState } from "react";
import {
  Container,
  Grid,
  Paper,
  TextField,
  Typography,
  Button,
  List,
  Switch,
  ListItem,
  ListItemText,
  Box,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMoreRounded";

export default function Dashboard() {
  const [location, setLocation] = useState("");
  const [price, setPrice] = useState("");
  const [area, setArea] = useState("");
  const [rooms, setRooms] = useState("");
  const [queries, setQueries] = useState([]);

  const handleAddQuery = () => {
    setQueries([...queries, { location, price, area, rooms }]);
    setLocation("");
    setPrice("");
    setArea("");
    setRooms("");
  };

  return (
    <>
      <CssBaseline />
      <Navbar />
      <Container>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ padding: 2 }}>
              <Typography variant="h6" gutterBottom>
                Parameters
              </Typography>
              <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
                <TextField
                  label="Location"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  fullWidth
                />
                <TextField
                  label="Price"
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                  fullWidth
                />
                <TextField
                  label="Area (sq meters)"
                  value={area}
                  onChange={(e) => setArea(e.target.value)}
                  fullWidth
                />
                <TextField
                  label="Rooms"
                  value={rooms}
                  onChange={(e) => setRooms(e.target.value)}
                  fullWidth
                />
                <Button variant="contained" onClick={handleAddQuery}>
                  Add Query
                </Button>
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ padding: 2 }}>
              <Typography variant="h6" gutterBottom>
                List of Queries
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
                        <ListItem>Price: {query.price}</ListItem>
                        <ListItem>Area: {query.area}</ListItem>
                        <ListItem>Rooms: {query.rooms}</ListItem>
                      </List>
                    </AccordionDetails>
                    <AccordionActions>
                      <Switch>Active/not</Switch>
                    </AccordionActions>
                  </Accordion>
                ))}
              </List>
            </Paper>
          </Grid>
          <Grid>
            <div>
              {/* 
              <ListItem key={index}>
                  <ListItemText
                    primary={`Location: ${query.location}, Price: ${query.price}, Area: ${query.area}`}
                  />
                </ListItem>
              */}
            </div>
          </Grid>
        </Grid>
      </Container>
    </>
  );
}
