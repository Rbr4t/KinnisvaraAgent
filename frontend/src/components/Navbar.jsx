import { AppBar, Toolbar, Typography, Button, Link, Box } from "@mui/material";
import { House } from "@mui/icons-material";

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
        }}
      >
        <Box>
          <Link href="/" style={{ color: "inherit", textDecoration: "none" }}>
            <Typography
              href="/"
              variant="h5"
              color="inherit"
              noWrap
              sx={{ flexGrow: 1 }}
            >
              <House />
              Kinnisvara äpp
            </Typography>
          </Link>
        </Box>

        {logitud ? (
          <Button
            href="/"
            onClick={logout}
            variant="contained"
            sx={{ my: 1, mx: 1.5 }}
          >
            Logi välja
          </Button>
        ) : (
          <Button href="/login" variant="contained" sx={{ my: 1, mx: 1.5 }}>
            Logi sisse
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
}
