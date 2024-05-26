import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import {
  Alert,
  Container,
  Typography,
  Box,
  Grid,
  Link,
  TextField,
  CssBaseline,
  Button,
  Avatar,
} from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { useState } from "react";

const defaultTheme = createTheme();

export default function SignUp() {
  const [error, setError] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const formData = {
      eesnimi: data.get("firstName"),
      perekonnanimi: data.get("lastName"),
      email: data.get("email"),
      parool: data.get("password"),
      paroolAgain: data.get("passwordAgain"),
    };
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (formData.eesnimi === "" || formData.perekonnanimi === "") {
      setError("Palun sisesta korrektsed eesnimi ja/või perekonnanimi.");
      return;
    }
    if (!emailRegex.test(formData.email)) {
      setError("Palun sisesta korrektne e-posti aadress.");
      return;
    }

    // Validate if passwords match
    if (formData.parool !== formData.paroolAgain && formData.parool != "") {
      setError("Sisestatud paroolid ei ühti.");
      return;
    }
    setError("");

    const sendReg = async () => {
      try {
        const response = await fetch("/auth/registreeri", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        window.location.href = "/login";
      } catch (error) {
        console.error("Error:", error);
      }
    };
    sendReg();
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Registreeri
          </Typography>

          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit}
            sx={{ mt: 3 }}
          >
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  autoComplete="given-name"
                  name="firstName"
                  type="text"
                  required
                  fullWidth
                  id="firstName"
                  label="Eesnimi"
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id="lastName"
                  label="Perekonnanimi"
                  name="lastName"
                  type="text"
                  autoComplete="family-name"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="email"
                  label="E-mail"
                  name="email"
                  type="email"
                  autoComplete="email"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="password"
                  label="Parool"
                  type="password"
                  id="password"
                  autoComplete="new-password"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="passwordAgain"
                  label="Parool uuesti"
                  type="password"
                  id="passwordAgain"
                />
              </Grid>
            </Grid>
            {error != "" ? <Alert severity="error">{error}</Alert> : null}
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Registreeri
            </Button>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="/login" variant="body2">
                  Kasutaja olemas? Logi sisse
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}
