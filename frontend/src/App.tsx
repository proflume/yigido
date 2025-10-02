import { useEffect, useMemo, useState } from "react";
import { Link, Route, Routes, useNavigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

function useAuthToken() {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem("token"));
  const navigate = useNavigate();
  useEffect(() => {
    if (!token) navigate("/login");
  }, [token, navigate]);
  return useMemo(
    () => ({
      token,
      setToken: (t: string | null) => {
        if (t) localStorage.setItem("token", t);
        else localStorage.removeItem("token");
        setToken(t);
      }
    }),
    [token]
  );
}

export default function App() {
  const auth = useAuthToken();
  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 24 }}>
      <header style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
        <Link to="/">Full Stack App</Link>
        {auth.token && (
          <button onClick={() => auth.setToken(null)}>Logout</button>
        )}
      </header>
      <Routes>
        <Route path="/login" element={<Login onAuth={auth.setToken} />} />
        <Route path="/" element={<Dashboard token={auth.token} />} />
      </Routes>
    </div>
  );
}
