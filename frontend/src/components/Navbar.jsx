import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Link,
  Box,
  Grid,
} from "@mui/material";
import { House } from "@mui/icons-material";
import SettingsIcon from "@mui/icons-material/Settings";
export default function Navbar() {
  let logitud = sessionStorage.getItem("access_token");

  const logout = async () => {
    sessionStorage.clear();
    window.location.href = "/";
  };

  return (
    <AppBar
      position="static"
      color="default"
      elevation={0}
      sx={{ borderBottom: (theme) => `1px solid ${theme.palette.divider}` }}
    >
      <Toolbar
        sx={{ flexWrap: "wrap" }}
        style={{
          display: "flex",
          justifyContent: "space-between",
          minHeight: "4rem",
          flexDirection: "row",
        }}
      >
        <Box justifyContent="center" alignItems="center">
          <Link
            href="/"
            style={{
              color: "inherit",
              textDecoration: "none",
              display: "flex",
              alignItems: "center",
            }}
          >
            <Button>
              <House fontSize="large" />
            </Button>
            <Typography
              href="/"
              variant="h5"
              color="inherit"
              alignContent="center"
              justifyItems="center"
              marginTop={1}
            >
              Kinnisvara äpp
            </Typography>
          </Link>
        </Box>

        {logitud ? (
          <Box>
            <Grid container justifyContent="center" alignItems="center">
              <Grid item>
                <Typography variant="h6" marginTop={1}>
                  Nimi Perekond
                </Typography>
              </Grid>
              <Grid item>
                <Button href="/settings">
                  <SettingsIcon fontSize="large" />
                </Button>
              </Grid>
              <Grid item>
                <Button
                  href="/"
                  onClick={logout}
                  variant="contained"
                  sx={{ my: 1, mx: 1.5 }}
                >
                  Logi välja
                </Button>
              </Grid>
            </Grid>
          </Box>
        ) : (
          <Button href="/login" variant="contained" sx={{ my: 1, mx: 1.5 }}>
            Logi sisse
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
}
