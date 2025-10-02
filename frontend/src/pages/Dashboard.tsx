import { useEffect, useMemo, useState } from "react";
import axios from "axios";

const API_URL = (import.meta as any).env.VITE_API_URL || "http://localhost:8000";

type Project = { id: number; name: string; description?: string };
type Task = { id: number; project_id: number; title: string; description?: string; is_done: boolean };

export default function Dashboard({ token }: { token: string | null }) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newProject, setNewProject] = useState("");
  const [newTask, setNewTask] = useState("");
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null);

  const client = useMemo(() => {
    const c = axios.create({ baseURL: API_URL });
    c.interceptors.request.use((config) => {
      if (token) config.headers.Authorization = `Bearer ${token}`;
      return config;
    });
    return c;
  }, [token]);

  useEffect(() => {
    if (!token) return;
    (async () => {
      const [{ data: ps }, { data: ts }] = await Promise.all([
        client.get("/projects/"),
        client.get("/tasks/")
      ]);
      setProjects(ps);
      setTasks(ts);
      setSelectedProjectId(ps[0]?.id ?? null);
    })();
  }, [token, client]);

  useEffect(() => {
    if (!token) return;
    const ws = new WebSocket(API_URL.replace("http", "ws") + "/ws/tasks");
    ws.onmessage = () => client.get("/tasks/").then(({ data }) => setTasks(data));
    return () => ws.close();
  }, [token, client]);

  async function addProject() {
    if (!newProject.trim()) return;
    const { data } = await client.post("/projects/", { name: newProject });
    setProjects((p) => [data, ...p]);
    setNewProject("");
  }

  async function addTask() {
    if (!newTask.trim() || !selectedProjectId) return;
    const { data } = await client.post("/tasks/", { project_id: selectedProjectId, title: newTask });
    setTasks((t) => [data, ...t]);
    setNewTask("");
  }

  async function toggleTask(task: Task) {
    const { data } = await client.patch(`/tasks/${task.id}`, { is_done: !task.is_done });
    setTasks((list) => list.map((t) => (t.id === task.id ? data : t)));
  }

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <section style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input placeholder="New project" value={newProject} onChange={(e) => setNewProject(e.target.value)} />
        <button onClick={addProject}>Add Project</button>
        <select value={selectedProjectId ?? undefined} onChange={(e) => setSelectedProjectId(Number(e.target.value))}>
          {projects.map((p) => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
      </section>
      <section style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input placeholder="New task" value={newTask} onChange={(e) => setNewTask(e.target.value)} />
        <button onClick={addTask} disabled={!selectedProjectId}>Add Task</button>
      </section>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {tasks
          .filter((t) => (selectedProjectId ? t.project_id === selectedProjectId : true))
          .map((t) => (
            <li key={t.id} style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <input type="checkbox" checked={t.is_done} onChange={() => toggleTask(t)} />
              <span>{t.title}</span>
            </li>
          ))}
      </ul>
    </div>
  );
}
