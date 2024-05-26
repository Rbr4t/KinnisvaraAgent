import SignIn from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import SignUp from "./pages/Register";
import Settings from "./pages/Settings";
import LandingPage from "./pages/Landing";
import Error from "./pages/Error";
import { Routes, Route } from "react-router-dom";
function App() {
  return (
    <Routes>
      <Route path="/" Component={LandingPage} />
      <Route path="/login" Component={SignIn} />
      <Route path="/register" Component={SignUp} />
      <Route path="/dashboard" Component={Dashboard} />
      <Route path="/settings" Component={Settings} />
      <Route path="*" Component={Error} />
    </Routes>
  );
}

export default App;
