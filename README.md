# PostgreSQL Query Service

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white">
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white">
  <img alt="Redis" src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white">
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
</picture>

**A production-ready query service for PostgreSQL with built-in caching, rate limiting, observability, and security layers.**

</div>

---

## Architecture

```
                          ┌─────────────────────────────────────────┐
                          │           Client Applications           │
                          │    React Frontend  ·  Swagger UI        │
                          └──────────────┬──────────────────────────┘
                                         │
                                    X-API-Key
                                   X-Unlock-Key
                                         │
                          ┌──────────────▼──────────────────────────┐
                          │          CORS Middleware                 │
                          │  Environment-aware origin selection      │
                          │  dev: ["*"]  ·  prod: explicit origins  │
                          └──────────────┬──────────────────────────┘
                                         │
                          ┌──────────────▼──────────────────────────┐
                          │        Rate Limiter Middleware           │
                          │     Per-IP sliding window (60s)         │
                          └──────────────┬──────────────────────────┘
                                         │
                          ┌──────────────▼──────────────────────────┐
                          │      Request Context Middleware          │
                          │   Captures source IP, endpoint, dest    │
                          └──────────────┬──────────────────────────┘
                                         │
                 ┌───────────────────────┬┴──────────────────────────┐
                 │                       │                           │
        ┌────────▼────────┐   ┌──────────▼──────────┐   ┌───────────▼──────────┐
        │   Query Routes  │   │  Mutation Routes    │   │  Observability       │
        │  SELECT · JOIN  │   │  INSERT · UPDATE    │   │  GET /GetLogs        │
        │  WHERE · GROUP  │   │  DELETE · DDL       │   │  GET /GetLogStats    │
        └────────┬────────┘   └──────────┬──────────┘   └───────────┬──────────┘
                 │                       │                           │
        ┌────────▼────────┐   ┌──────────▼──────────┐               │
        │  SQLi Validator │   │  Cache Invalidation │               │
        │  Parameterized  │   │   Pattern-based     │               │
        └────────┬────────┘   └──────────┬──────────┘               │
                 │                       │                           │
                 └───────────┬───────────┘                           │
                             │                                       │
                 ┌───────────▼───────────┐              ┌────────────▼───────────┐
                 │    Request Executor   │              │   Observability Table  │
                 │  Connection pooling   │──────log────▶│   observability_logs   │
                 │  Error classification │              │   (auto-created)       │
                 └───────────┬───────────┘              └────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼──────┐ ┌────▼─────┐ ┌──────▼──────┐
     │  PostgreSQL   │ │  Upstash │ │   Loguru    │
     │  (psycopg2)   │ │  Redis   │ │  Console    │
     │  Cloud / Local│ │  Cache   │ │  Logging    │
     └───────────────┘ └──────────┘ └─────────────┘
```

---

## Features

### Security

| Layer | Description |
|-------|-------------|
| **API Key Auth** | Header-based authentication via `X-API-Key`. Requests without a valid key are rejected with `401`. When no key is configured, auth is disabled (dev mode). |
| **Unlock Key** | Secondary `X-Unlock-Key` header for additional access control on sensitive routes. |
| **SQLi Prevention** | Every route runs input through regex-based SQLi pattern detection before query execution. All queries use `psycopg2.sql` for parameterized identifier and value binding. |
| **Rate Limiting** | Per-IP sliding window rate limiter (configurable via `RATE_LIMIT_PER_MINUTE`). Excess requests receive `429 Too Many Requests`. |

### Performance

| Layer | Description |
|-------|-------------|
| **Redis Caching** | Query results are cached in Upstash Redis with configurable TTL (default 1200s). Cache misses execute the query and store the result. The app gracefully degrades if Redis is unavailable. |
| **Cache Invalidation** | Mutations (`INSERT`, `UPDATE`, `DELETE`) automatically invalidate related cache keys using pattern-based `SCAN` + `DELETE`. |
| **Connection Pooling** | `psycopg2.pool.ThreadedConnectionPool` with configurable `minconn`/`maxconn`. Connections are reused across requests. |
| **Multi-stage Docker** | Builder stage compiles wheels, runtime stage uses `python:3.12-slim` with only runtime dependencies. `.dockerignore` excludes `venv/`, `.git/`, `__pycache__/`. |

### Observability

| Layer | Description |
|-------|-------------|
| **Event Logging** | Every request outcome (success, error, sql_error) is logged to the `observability_logs` table with HTTP status, endpoint, source/destination IPs, message, and timestamp. |
| **Log Query API** | `GET /GetLogs` — server-side pagination, sorting, and filtering by log type, endpoint, HTTP status, and message search. |
| **Aggregated Stats** | `GET /GetLogStats` — hourly bucketed counts by log type, powering the frontend's time-series charts. |
| **Console Logging** | Loguru writes to stdout/stderr alongside database persistence. |

### Observability Table Schema

```sql
CREATE TABLE IF NOT EXISTS observability_logs (
    id             SERIAL PRIMARY KEY,
    http_status    INTEGER NOT NULL,
    log_type       VARCHAR(20) NOT NULL,    -- success, error, sql_error, info
    endpoint       VARCHAR(255) NOT NULL,
    source_ip      VARCHAR(45),
    destination_ip VARCHAR(45),
    message        TEXT,
    created_at     TIMESTAMP DEFAULT now()
);
```

### Environment-Aware Configuration

```
┌──────────────────────────────────────────────────────────┐
│                    ENVIRONMENT check                     │
│                                                          │
│   ┌─────────────────┐         ┌────────────────────┐    │
│   │   development   │         │    production       │    │
│   │                 │         │                     │    │
│   │  CORS: ["*"]    │         │  CORS: [WEBHOST,    │    │
│   │  All origins    │         │    ALLOWED_ORIGINS]  │    │
│   │  allowed        │         │  Explicit origins   │    │
│   │                 │         │  only               │    │
│   └─────────────────┘         └────────────────────┘    │
│                                                          │
│   Falls back to development when ENVIRONMENT is unset    │
└──────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Local Development

```bash
# 1. Clone and install
git clone <repo-url> && cd postgresql-query-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your POSTGRES_URL, API_KEY, etc.

# 3. Run
python app/run.py
# → http://localhost:8000/docs
```

### Docker

```bash
docker compose up --build
# → Backend on http://localhost:8000
# → PostgreSQL on localhost:5432
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ENVIRONMENT` | Yes | `development` or `production` |
| `POSTGRES_URL` | Yes | PostgreSQL connection string |
| `WEBHOST` | Recommended | Frontend origin for CORS |
| `API_KEY` | Recommended | Shared API key for authentication |
| `UNLOCK_KEY` | Optional | Secondary auth key |
| `UPSTASH_REDIS_REST_URL` | Optional | Upstash Redis REST endpoint |
| `UPSTASH_REDIS_TOKEN` | Optional | Upstash Redis auth token |
| `ALLOWED_ORIGINS` | Optional | Comma-separated additional CORS origins |
| `RATE_LIMIT_PER_MINUTE` | Optional | Max requests per IP per minute (default: 60) |

---

## Request Flow

```
Client Request
    │
    ▼
┌─────────────┐   No     ┌──────────────┐
│  Valid       │────────▶ │  401         │
│  API Key?   │          │  Unauthorized │
└──────┬──────┘          └──────────────┘
       │ Yes
       ▼
┌─────────────┐   Yes    ┌──────────────┐
│  Rate limit │────────▶ │  429         │
│  exceeded?  │          │  Too Many    │
└──────┬──────┘          └──────────────┘
       │ No
       ▼
┌─────────────┐   Yes    ┌──────────────┐
│  SQLi       │────────▶ │  422         │
│  detected?  │          │  Rejected    │
└──────┬──────┘          └──────────────┘
       │ No
       ▼
┌─────────────┐   Hit    ┌──────────────┐
│  Redis      │────────▶ │  Return      │
│  cache?     │          │  cached data │
└──────┬──────┘          └──────────────┘
       │ Miss
       ▼
┌─────────────┐          ┌──────────────┐
│  Execute    │────────▶ │  Cache +     │
│  query      │          │  return data │
└──────┬──────┘          └──────────────┘
       │
       ▼
  Log to observability_logs
```

---

## API Reference

### Connection

<details>
<summary><strong>POST /Connection</strong></summary>

Verifies database connectivity. Returns a lightweight test query result.

**Response:**
```json
{
  "status": "OK",
  "message": "Connection established.",
  "test_query_result": [1]
}
```

</details>

### Select Queries

<details>
<summary><strong>POST /GetAll</strong></summary>

Returns all rows from a table. Results are cached for 20 minutes.

```json
{ "table": "users" }
```

</details>

<details>
<summary><strong>POST /GetAllOrderBy</strong></summary>

Returns all rows ordered by a column.

```json
{ "table": "users", "order": "created_at" }
```

</details>

<details>
<summary><strong>POST /GetAllWithLimit</strong></summary>

Returns rows with a limit.

```json
{ "table": "users", "limit": 50 }
```

</details>

<details>
<summary><strong>POST /GetAllWithLimitAndOffset</strong></summary>

Returns rows with limit and offset for pagination.

```json
{ "table": "users", "limit": 25, "offset": 50 }
```

</details>

<details>
<summary><strong>POST /GetAllWhere</strong></summary>

Returns rows matching WHERE conditions. Conditions use `column operator value` syntax.

```json
{ "table": "users", "conditions": ["age >= 18", "status = active"] }
```

</details>

<details>
<summary><strong>POST /GetAllWhereAndOrderBy</strong></summary>

WHERE conditions with ordering.

```json
{ "table": "users", "conditions": ["status = active"], "order": "name" }
```

</details>

<details>
<summary><strong>POST /GetAllBetween</strong></summary>

Returns rows where a column value falls between start and end.

```json
{ "table": "orders", "column": "created_at", "start": "2024-01-01", "end": "2024-12-31" }
```

</details>

<details>
<summary><strong>POST /GetAllWhereMatches</strong></summary>

Returns rows matching a LIKE pattern (`%` wildcards).

```json
{ "table": "users", "column": "name", "wild_card": "%john%" }
```

</details>

<details>
<summary><strong>POST /GetAllWhereIn</strong></summary>

Returns rows where column value is IN a list.

```json
{ "table": "users", "column": "status", "search_parameters": ["active", "pending"] }
```

</details>

<details>
<summary><strong>POST /GetAllWhereAndCount</strong></summary>

Counts rows matching a condition.

```json
{ "table": "orders", "primary_column": "id", "secondary_column": "status", "search_parameter": "shipped" }
```

</details>

<details>
<summary><strong>POST /GetAllWhereAverage</strong></summary>

Returns the average of a numeric column.

```json
{ "table": "orders", "column": "total", "search_parameters": ["shipped", "delivered"] }
```

</details>

<details>
<summary><strong>POST /GetAllGroupBy</strong></summary>

Groups by a column and counts.

```json
{ "table": "orders", "primary_column": "id", "secondary_column": "status" }
```

</details>

### Column-Specific Queries

<details>
<summary><strong>POST /GetByColumns</strong></summary>

Select specific columns only.

```json
{ "table": "users", "columns": ["name", "email"] }
```

</details>

<details>
<summary><strong>POST /GetByColumnsAndOrderBy</strong></summary>

Select specific columns with ordering.

```json
{ "table": "users", "columns": ["name", "email"], "order": "name" }
```

</details>

<details>
<summary><strong>POST /GetByColumnsAndLimit</strong></summary>

Select specific columns with a limit.

```json
{ "table": "users", "columns": ["name", "email"], "limit": 100 }
```

</details>

### Joins

<details>
<summary><strong>POST /GetTableJoin</strong></summary>

Join two tables on a common key. Supports `INNER`, `LEFT`, `RIGHT`, `FULL` join types via `?join_type=` query param.

```json
{
  "columns": ["a.name", "b.email"],
  "primary_table": "users",
  "secondary_table": "contacts",
  "common_key": "user_id"
}
```

</details>

<details>
<summary><strong>POST /SubQueryExists</strong></summary>

Subquery with EXISTS/NOT EXISTS via `?operator=` query param.

```json
{
  "primary_column": "id",
  "primary_table": "users",
  "sub_query_select": "user_id",
  "sub_query_table": "orders",
  "sub_query_where_column": "status",
  "sub_query_where_value": "active"
}
```

</details>

### Mutations

<details>
<summary><strong>POST /CreateOne</strong></summary>

Insert a single row. Invalidates related cache.

```json
{ "table": "users", "columns": ["name", "email"], "values": ["Jane", "jane@example.com"] }
```

</details>

<details>
<summary><strong>POST /CreateMany</strong></summary>

Insert multiple rows in one operation.

```json
{
  "table": "users",
  "columns": ["name", "email"],
  "values": [
    ["Jane", "jane@example.com"],
    ["John", "john@example.com"]
  ]
}
```

</details>

<details>
<summary><strong>POST /UpdateOne</strong></summary>

Update a single row.

```json
{
  "table": "users",
  "secondary_column": "name",
  "set_value": "Jane Doe",
  "primary_column": "id",
  "where_value": "1"
}
```

</details>

<details>
<summary><strong>POST /UpdateMany</strong></summary>

Update multiple columns for rows matching a condition.

```json
{
  "table": "users",
  "set_columns": ["status", "updated_at"],
  "set_values": ["active", "2024-01-01"],
  "where_column": "country",
  "where_value": "USA"
}
```

</details>

<details>
<summary><strong>POST /DeleteById</strong></summary>

Delete a single row by ID.

```json
{ "table": "users", "primary_column": "id", "id": 42 }
```

</details>

<details>
<summary><strong>POST /DeleteMany</strong></summary>

Delete multiple rows by a list of IDs.

```json
{ "table": "users", "primary_column": "id", "primary_key": [1, 2, 3] }
```

</details>

### DDL

<details>
<summary><strong>POST /CreateTable</strong></summary>

Create a new table with column definitions.

```json
{
  "table_name": "analytics",
  "column_names_with_properties": [
    "id SERIAL PRIMARY KEY",
    "name VARCHAR(255) NOT NULL",
    "email VARCHAR(255) UNIQUE",
    "created_at TIMESTAMP DEFAULT now()"
  ]
}
```

</details>

### Observability

<details>
<summary><strong>GET /GetLogs</strong></summary>

Query event logs with server-side pagination, sorting, and filtering.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | int | 25 | Page size |
| `offset` | int | 0 | Pagination offset |
| `log_type` | string | | Filter: `success`, `error`, `sql_error`, `info` |
| `endpoint` | string | | Filter by endpoint (partial match) |
| `http_status` | int | | Filter by HTTP status code |
| `search` | string | | Search message text |
| `sort_by` | string | `created_at` | Sort column |
| `sort_order` | string | `desc` | `asc` or `desc` |

</details>

<details>
<summary><strong>GET /GetLogStats</strong></summary>

Aggregated hourly counts by log type for time-series charts.

**Response:**
```json
{
  "result": [
    { "time_bucket": "2024-06-27T10:00:00", "log_type": "success", "count": 42 },
    { "time_bucket": "2024-06-27T10:00:00", "log_type": "error", "count": 3 }
  ]
}
```

</details>

### Scheduled Reports

<details>
<summary><strong>POST /QueryDownload</strong></summary>

Execute a query and email the results as a CSV/Excel file. Powered by Celery.

```json
{
  "query": "SELECT id, name, email FROM users WHERE created_at >= '2024-01-01'",
  "file_name": "users_export.xlsx",
  "recipient": ["ops@example.com"],
  "sender": "no-reply@example.com",
  "password": "smtp_password",
  "role": ["admin"],
  "subject": "Monthly Export",
  "message": "Attached is the users export.",
  "email_server": "smtp.example.com"
}
```

</details>

---

## Security

### SQLi Prevention

All user input passes through a two-layer defense:

1. **Regex pattern detection** — catches common injection patterns (`UNION`, `DROP`, `--`, `' OR '1'='1'`, etc.) before the query is built
2. **Parameterized queries** — all values are bound via `psycopg2.sql.SQL` / `sql.Identifier` / `sql.Placeholder`. Table and column names are validated against `^[a-zA-Z_][a-zA-Z0-9_]*$`

### Error Handling

Errors are classified by type and mapped to appropriate HTTP responses:

| psycopg2 Error | HTTP Status | Log Type |
|---------------|-------------|----------|
| `SyntaxError` | 422 | `sql_error` |
| `ConnectionFailure` | 503 | `error` |
| `UndefinedTable` | 404 | `sql_error` |
| `DuplicateTable` | 409 | `sql_error` |
| `UniqueViolation` | 409 | `sql_error` |
| `InternalError` | 500 | `error` |

---

## License

[MIT](LICENSE)
