import { Alert, Box, AlertTitle, CssBaseline, Grid } from "@mui/material";
import Navbar from "../components/Navbar";

const NotFoundPage = ({ error_code = 404 }) => {
  const handleGoHome = () => {
    console.log("nah");
  };

  return (
    <Box>
      <CssBaseline />

      <Navbar />
      <Grid
        container
        direction="column"
        alignItems="center"
        justifyContent="center"
        sx={{ minHeight: "90vh" }}
        padding={10}
      >
        <Grid item xs={1}>
          <Alert
            variant="filled"
            severity="error"
            sx={{ width: "100%", maxWidth: 500 }}
          >
            <AlertTitle>{error_code}</AlertTitle>
            Mingi viga props
          </Alert>
        </Grid>
      </Grid>
    </Box>
  );
};

export default NotFoundPage;
