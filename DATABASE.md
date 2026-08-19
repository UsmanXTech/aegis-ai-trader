# Database

## Technology

Aegis uses Python's built-in `sqlite3` module through `src/aegis/store.py`.

Default database path:

```text
data/aegis.db
```

`AegisStore` creates the parent directory when needed and initializes the schema automatically when instantiated.

## Architecture

The database is a small **event store**, not a normalized trading database:

```text
Trading components
      ↓
TradeJournal / AegisStore
      ↓
SQLite events
      ↓
FastAPI read endpoints
      ↓
Dashboard
```

## Tables

### `events`

**Purpose:** Persist decisions, account snapshots, orders, positions, P&L, rejections, prepared trades, and other application events as JSON payloads.

| Field | Type | Constraints | Purpose |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Event identifier/order |
| `event_type` | TEXT | NOT NULL | Event category |
| `created_at` | TEXT | NOT NULL, default `CURRENT_TIMESTAMP` | Insert timestamp |
| `payload` | TEXT | NOT NULL | JSON-encoded event data |

The exact set of event types is not enforced by a database constraint. Existing code uses types including `account`, `decision`, `rejected`, and `prepared`; API endpoints also query `order`, `position`, and `pnl`.

## Indexes

The store creates:

```sql
CREATE INDEX IF NOT EXISTS idx_events_type_time
    ON events(event_type, created_at);
```

The primary key also supplies the SQLite rowid-backed primary-key access path.

## Relationships

There are no foreign-key relationships. Event relationships are represented implicitly through JSON payloads and application logic.

## Connection behavior

Each store operation opens a SQLite connection with `sqlite3.connect(self.path)`, uses `sqlite3.Row` as the row factory, and closes the connection through a context manager.

Writes use parameterized SQL:

```sql
INSERT INTO events(event_type, payload) VALUES (?, ?)
```

## Serialization

`AegisStore.append()` serializes payloads using `json.dumps(..., default=str, separators=(",", ":"))`. This permits otherwise non-JSON-native values to be stringified, which is convenient for journaling but means payload schema is not database-enforced.

## Query behavior

`recent()` can filter by `event_type` and returns newest rows first by `id`. It validates that `limit >= 1`.

The FastAPI layer exposes this through `/api/v1/events`, `/account`, `/decisions`, `/orders`, `/positions`, and `/pnl` views.

## Migrations

There is currently **no migration framework**. Schema initialization is performed by `AegisStore._initialize()` with `CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS` statements.

If the schema evolves, add a deliberate migration strategy before introducing incompatible changes. Update this document and tests.

## Seed data

No verified seed-data mechanism exists in the repository.

## Data ownership

The store is owned by the Aegis application and serves as an operational journal/read model. It is not a replacement for Alpaca's authoritative account/order/position records.

## Important limitation

Because the database stores heterogeneous JSON events rather than normalized entities, changing event payload shapes can break API/dashboard consumers without producing a database error. Treat event schemas as compatibility contracts and update tests/documentation when they change.
