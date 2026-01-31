# Production Line OEE Tracker

Track Overall Equipment Effectiveness across CNC machines and shifts.

## Architecture

```mermaid
flowchart LR
    CLI["CLI (Typer)<br/>User commands"] --> CRUD["CRUD (crud.py)<br/>Business logic & OEE calculations"]
    CRUD --> Models["Models (SQLAlchemy)<br/>Machine, Shift, ProductionRun, etc."]
    Models --> DB[("PostgreSQL<br/>Data storage")]
```

## Setup

```bash
# 1. Install dependencies
uv sync

# 2. Install CLI globally
uv pip install -e .

# 3. Start PostgreSQL (via Docker)
docker compose up -d

# 4. Run migrations
alembic upgrade head

# 5. Load sample data (optional)
load-sample

# 6. Use CLI
oee --help
```

## CLI Commands

```bash
# Machines
oee machine list
oee machine create "CNC-001" 30.5 --loc "Bay A"
oee machine get 1
oee machine update 1 --name "CNC-001-Updated"
oee machine delete 1

# Shifts
oee shift list
oee shift create "Day Shift"

# Operators
oee operator list
oee operator create "John Smith"

# Production Runs
oee run list
oee run create 1 1 1 "2025-01-06 06:00:00" "2025-01-06 14:00:00"
oee run start 1
oee run stop 1 500 10
oee run active

# Downtime Events
oee downtime create 1 SETUP
oee downtime stop 1
oee downtime list --run-id 1
oee downtime active

# Reports
oee report oee 1
oee report machine 1 --start 2025-01-06 --end 2025-01-10
oee report shift 1
oee report machines
oee report shifts
oee report downtime --limit 10
```

## Database

```mermaid
erDiagram
    machines {
        int id PK
        string name
        float ideal_cycle_time
        string location
    }

    shifts {
        int id PK
        string name
    }

    operators {
        int id PK
        string name
    }

    reason_codes {
        string code PK
        string description
        bool is_planned
    }

    production_runs {
        int id PK
        int machine_id FK
        int shift_id FK
        int operator_id FK
        datetime planned_start_time
        datetime planned_end_time
        datetime actual_start_time
        datetime actual_end_time
        int good_parts_count
        int rejected_parts_count
    }

    downtime_events {
        int id PK
        int production_run_id FK
        string reason_code FK
        datetime start_time
        datetime end_time
    }

    machines ||--o{ production_runs : "has"
    shifts ||--o{ production_runs : "has"
    operators ||--o{ production_runs : "runs"
    production_runs ||--o{ downtime_events : "has"
    reason_codes ||--o{ downtime_events : "categorizes"
```

## OEE Formula

- **Availability** = Run Time / Planned Production Time
- **Performance** = (Ideal Cycle Time × Total Parts) / Run Time
- **Quality** = Good Parts / Total Parts
- **OEE** = Availability × Performance × Quality

## TODO

| Description | File | Function |
|-------------|------|----------|
| Add unique constraint on machine name | `oee_tracker/models.py` | `Machine` |
| Create migration for unique constraint | `migrations/versions/` | `alembic revision` |
| Handle IntegrityError for duplicate name on update | `oee_tracker/crud.py` | `update_machine` |
| Add is_admin column to operators | `oee_tracker/models.py` | `Operator` |
| Create migration for is_admin column | `migrations/versions/` | `alembic revision` |
| Implement is_admin check in delete_machine | `oee_tracker/crud.py` | `delete_machine` |
| Move load-sample to subcommand pattern | `oee_tracker/cli/` | `data load` |
| Add optional sort key parameter to list functions | `oee_tracker/crud.py` | `get_all_*` |
