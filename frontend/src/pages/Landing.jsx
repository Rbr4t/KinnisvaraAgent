import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Container,
  Grid,
  Paper,
  Box,
  CssBaseline,
} from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Navbar from "../components/Navbar"; // Assuming you have a Navbar component
import Carousel from "../components/Carousel";

const theme = createTheme({
  palette: {
    primary: {
      main: "#1976d2",
    },
    secondary: {
      main: "#ff4081",
    },
  },
});

const LandingPage = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Navbar />
      <Container maxWidth="lg">
        <HeroSection />
        <FeaturesSection />
        <Footer />
      </Container>
    </ThemeProvider>
  );
};

const HeroSection = () => {
  return (
    <Box
      sx={{
        textAlign: "center",
        py: 6,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <Typography variant="h3" component="h1" gutterBottom>
        Saa tuttavaks! Sinu isiklik kinnisvaramaakler 🔑
      </Typography>
      <Typography variant="h6" component="p" gutterBottom>
        Ta aitab sul leida kõige sobivama korteri sinu nõudmiste järgi.
      </Typography>
      <Button
        variant="contained"
        color="primary"
        size="large"
        href="/dashboard"
      >
        Alusta
      </Button>
    </Box>
  );
};

const FeaturesSection = () => {
  const features = [
    {
      title: "🔥 Hoian silma peal 🔥",
      description:
        "Skännin kõiki Eesti suurimaid kinnisvara portaale ja teavitan sind, kui leian korteri!",
    },
    {
      title: "⚡ Olen paindlik! ⚡",
      description: "Leian korteri sinu nõudmiste järgi.",
    },
    {
      title: "🧠 Olen nutikas 🧠",
      description: "Leian ka korterid, mis võiksid sulle huvi pakkuda!",
    },
  ];

  return (
    <Box sx={{ py: 6 }}>
      <Carousel features={features} />
    </Box>
  );
};

const Footer = () => {
  return (
    <Box
      sx={{
        py: 3,
        mt: 6,
        borderTop: "1px solid #ddd",
        textAlign: "center",
      }}
    >
      <Typography variant="body1">&copy; {new Date().getFullYear()}</Typography>
    </Box>
  );
};

export default LandingPage;
