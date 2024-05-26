import { useState } from "react";
import {
  Container,
  Grid,
  Paper,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CssBaseline,
  Box,
} from "@mui/material";
import Navbar from "../components/Navbar";

export default function Settings() {
  const [intensity, setIntensity] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  const handleIntensityChange = (event) => {
    setIntensity(event.target.value);
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePhoneChange = (event) => {
    setPhone(event.target.value);
  };

  const handleAddMoney = () => {
    // Implement add money logic here
    alert("Add money functionality to be implemented");
  };

  const handleLogout = () => {
    // Implement logout logic here
    alert("Logout functionality to be implemented");
  };

  const handleSave = () => {
    const settings = {
      intensity,
      email,
      phone,
    };
    console.log("Saved Settings:", settings);
    alert("Settings saved!");
  };

  return (
    <>
      <CssBaseline />
      <Navbar />
      <Container>
        <Grid
          container
          spacing={3}
          justifyContent="center"
          sx={{ marginTop: 4 }}
        >
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ padding: 2 }}>
              <Typography variant="h6" gutterBottom>
                Seaded
              </Typography>
              <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
                <TextField
                  label="Email"
                  value={email}
                  onChange={handleEmailChange}
                  fullWidth
                />
                <TextField
                  label="Phone Number"
                  value={phone}
                  onChange={handlePhoneChange}
                  fullWidth
                />
                <Button variant="contained" onClick={handleAddMoney}>
                  Lisa raha
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSave}
                >
                  Salvesta
                </Button>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </>
  );
}
