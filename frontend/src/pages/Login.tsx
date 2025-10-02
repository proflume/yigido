import { useState } from "react";
import axios from "axios";

const API_URL = (import.meta as any).env.VITE_API_URL || "http://localhost:8000";

export default function Login({ onAuth }: { onAuth: (token: string) => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      const form = new FormData();
      form.append("username", email);
      form.append("password", password);
      const { data } = await axios.post(`${API_URL}/auth/token`, form);
      onAuth(data.access_token);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Login failed");
    }
  }

  return (
    <form onSubmit={handleLogin} style={{ display: "grid", gap: 8 }}>
      <h2>Login</h2>
      <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Sign in</button>
      {error && <div style={{ color: "red" }}>{error}</div>}
    </form>
  );
}
