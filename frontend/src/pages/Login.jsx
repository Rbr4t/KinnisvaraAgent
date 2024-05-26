import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import {
  Button,
  Avatar,
  CssBaseline,
  TextField,
  Link,
  Grid,
  Box,
  Typography,
  Container,
  Alert,
} from "@mui/material";
import { useState } from "react";
import Navbar from "../components/Navbar";

const defaultTheme = createTheme();

export default function SignIn() {
  const [fail, setFail] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const formData = {
      email: data.get("email"),
      parool: data.get("parool"),
    };
    const sendReg = async () => {
      try {
        const response = await fetch("/auth/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });

        if (response.ok) {
          const responseData = await response.json();
          sessionStorage.setItem("access_token", responseData.access_token);
          setFail(false);
          window.location.href = "/dashboard";
        } else {
          setFail(true);
          throw new Error("Network response was not ok");
        }
      } catch (error) {
        setFail(true);
        console.error("Error:", error);
      }
    };
    sendReg();
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Navbar />

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
            Logi sisse
          </Typography>
          <Box
            component="form"
            onSubmit={handleSubmit}
            noValidate
            sx={{ mt: 1 }}
          >
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email"
              name="email"
              type="text"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="parool"
              label="Parool"
              type="password"
              id="password"
              autoComplete="current-password"
            />

            {fail ? (
              <Alert severity="error">Sisselogimine ebaõnnestus</Alert>
            ) : null}

            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Logi sisse
            </Button>
            <Grid container>
              <Grid item>
                <Link href="/register" variant="body2">
                  Puudub kasutaja? Registreeri
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}
