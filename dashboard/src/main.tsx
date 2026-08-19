import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";
import type { AccountEvent, Event } from "./types";

const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function App() {
  const [health, setHealth] = useState("checking");
  const [events, setEvents] = useState<Event[]>([]);
  const [account, setAccount] = useState<AccountEvent | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [healthResponse, eventResponse, accountResponse] = await Promise.all([
          fetch(`${API}/health`),
          fetch(`${API}/api/v1/events?limit=20`),
          fetch(`${API}/api/v1/account?limit=1`),
        ]);
        setHealth(healthResponse.ok ? "online · paper" : "offline");
        setEvents(await eventResponse.json());
        const rows: Array<{ payload: string }> = await accountResponse.json();
        setAccount(rows.length ? JSON.parse(rows[0].payload) : null);
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
        <div><span className="eyebrow">AUTONOMOUS OPTIONS AGENT</span><h1>Aegis</h1></div>
        <span className="status">● {health}</span>
      </header>

      <section className="grid">
        <article><span>EQUITY</span><strong>{account ? `$${account.equity.toLocaleString()}` : "—"}</strong></article>
        <article><span>DAILY P&L</span><strong>{account ? `$${account.daily_pnl.toFixed(2)}` : "—"}</strong></article>
        <article><span>BUYING POWER</span><strong>{account ? `$${account.buying_power.toLocaleString()}` : "—"}</strong></article>
        <article><span>POSITIONS</span><strong>{account?.open_positions ?? "—"}</strong></article>
      </section>

      <section className="panel">
        <div className="panel-head"><h2>Decision Journal</h2><span>Last 20 events</span></div>
        {events.length === 0 ? <p className="muted">No events recorded yet.</p> : (
          <div className="events">
            {events.map((event) => (
              <div className="event" key={event.id}>
                <b>{event.event_type}</b><code>{event.payload}</code><small>{event.created_at}</small>
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<React.StrictMode><App /></React.StrictMode>);
