# API Reference

The HTTP API is implemented in [`src/aegis/api.py`](src/aegis/api.py) using FastAPI. The application is created as `app = FastAPI(title="Aegis AI Trader API", version="0.1.0")`.

## Authentication

No authentication or authorization dependency is declared in `api.py` for the discovered endpoints. Whether deployment places the API behind an authenticated network boundary is **Unknown**.

Do not expose this API publicly without reviewing its security model.

## Endpoints

### GET `/health`

**Purpose:** Basic service health/mode check.

**Authentication:** None in the application code.

**Request:** No body or query parameters.

**Response:**

```json
{"status":"ok","mode":"paper"}
```

**Implementation:** `src/aegis/api.py::health`

---

### GET `/api/v1/events`

**Purpose:** Return recent persisted events.

**Authentication:** None in the application code.

**Query parameters:**

| Parameter | Type | Default | Constraints |
|---|---|---:|---|
| `event_type` | string/null | null | Optional event filter |
| `limit` | integer | 50 | 1–500 |

**Response:** Array of event rows from `AegisStore.recent()`.

**Implementation:** `src/aegis/api.py::events`

---

### GET `/api/v1/account`

**Purpose:** Return recent events with `event_type="account"`.

**Authentication:** None in the application code.

**Query parameters:** `limit` integer, default 1, range 1–20.

**Response:** Array of persisted event rows.

**Implementation:** `src/aegis/api.py::account`

---

### GET `/api/v1/decisions`

**Purpose:** Return recent decision events.

**Authentication:** None in the application code.

**Query parameters:** `limit` integer, default 50, range 1–500.

**Response:** Array of persisted event rows.

**Implementation:** `src/aegis/api.py::decisions`

---

### GET `/api/v1/orders`

**Purpose:** Return recent order events.

**Authentication:** None in the application code.

**Query parameters:** `limit` integer, default 50, range 1–500.

**Response:** Array of persisted event rows.

**Implementation:** `src/aegis/api.py::orders`

---

### GET `/api/v1/positions`

**Purpose:** Return recent position events.

**Authentication:** None in the application code.

**Query parameters:** `limit` integer, default 50, range 1–500.

**Response:** Array of persisted event rows.

**Implementation:** `src/aegis/api.py::positions`

---

### GET `/api/v1/pnl`

**Purpose:** Return recent P&L events.

**Authentication:** None in the application code.

**Query parameters:** `limit` integer, default 100, range 1–500.

**Response:** Array of persisted event rows.

**Implementation:** `src/aegis/api.py::pnl`

## API data model

The API exposes SQLite event rows rather than separate typed HTTP resources. A row contains:

- `id` — integer primary key.
- `event_type` — event category.
- `created_at` — SQLite current timestamp when inserted.
- `payload` — JSON string containing the event-specific data.

See [`DATABASE.md`](DATABASE.md).

## API conventions and limitations

- All currently discovered routes are GET/read routes.
- There is no pagination cursor; callers use bounded `limit` values.
- There is no documented authentication layer.
- There are no verified OpenAPI customization or deployment proxy rules beyond FastAPI defaults.
- New routes should be added with tests and documented here.
