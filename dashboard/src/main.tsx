import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

type Event = { id: number; event_type: string; created_at: string; payload: string };

const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function App() {
  const [health, setHealth] = useState("checking");
  const [events, setEvents] = useState<Event[]>([]);

  useEffect(() => {
    const load = async () => {
      try {
        const [healthResponse, eventResponse] = await Promise.all([
          fetch(`${API}/health`),
          fetch(`${API}/api/v1/events?limit=20`),
        ]);
        setHealth(healthResponse.ok ? "online · paper" : "offline");
        setEvents(await eventResponse.json());
      } catch {
        setHealth("API unavailable");
      }
    };
    load();
    const timer = window.setInterval(load, 10000);
    return () => window.clearInterval(timer);
  }, []);

  return (
    <main>
      <header>
        <div>
          <span className="eyebrow">AUTONOMOUS OPTIONS AGENT</span>
          <h1>Aegis</h1>
        </div>
        <span className="status">● {health}</span>
      </header>

      <section className="grid">
        <article><span>MODE</span><strong>PAPER</strong></article>
        <article><span>ENGINE</span><strong>RUNNING</strong></article>
        <article><span>EVENTS</span><strong>{events.length}</strong></article>
        <article><span>LIVE TRADING</span><strong>DISABLED</strong></article>
      </section>

      <section className="panel">
        <div className="panel-head"><h2>Decision Journal</h2><span>Last 20 events</span></div>
        {events.length === 0 ? <p className="muted">No events recorded yet.</p> : (
          <div className="events">
            {events.map((event) => (
              <div className="event" key={event.id}>
                <b>{event.event_type}</b>
                <code>{event.payload}</code>
                <small>{event.created_at}</small>
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<React.StrictMode><App /></React.StrictMode>);
