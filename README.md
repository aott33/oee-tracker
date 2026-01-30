# Production Line OEE Tracker

Track Overall Equipment Effectiveness across CNC machines and shifts.

## Architecture

```mermaid
flowchart TD
    subgraph Startup["1. Startup"]
        A[uv sync] --> B[Install Dependencies]
        B --> C[docker compose up -d]
        C --> D[PostgreSQL Container Running]
    end

    subgraph Database["2. Database Setup"]
        D --> E[db.py loads .env]
        E --> F[create_engine connects to PostgreSQL]
        F --> G[SessionLocal factory created]
    end

    subgraph Migrations["3. Migrations"]
        G --> H[uv run alembic upgrade head]
        H --> I[Alembic reads models.py]
        I --> J[Base.metadata defines tables]
        J --> K[Tables created in PostgreSQL]
    end

    subgraph SampleData["4. Load Sample Data"]
        K --> L[uv run load-sample]
        L --> M[sample/load.py executes]
        M --> N[get_session from db.py]
        N --> O[Read CSV files]
        O --> P[Create model instances]
        P --> Q[session.add + commit]
        Q --> R[Data in PostgreSQL]
    end

    subgraph CLI["5. Run CLI"]
        R --> S[uv run oee-tracker]
        S --> T[cli.py main executes]
        T --> U["CLI for OEE Tracker<br/>(Not yet implemented)"]
    end

    subgraph Models["models.py (ORM Layer)"]
        Machine
        Shift
        Operator
        ReasonCode
        ProductionRun
        DowntimeEvent
    end

    subgraph CRUD["crud.py (Business Logic)"]
        CreateOps[Create Operations]
        ReadOps[Read/Query Operations]
        UpdateOps[Update Operations]
        DeleteOps[Delete Operations]
        OEECalc[OEE Calculations]
    end

    U -.->|will use| CRUD
    CRUD --> Models
    Models --> G
```

## Setup

```bash
# 1. Install dependencies
uv sync

# 2. Start PostgreSQL (via Docker)
docker compose up -d

# 3. Run migrations
uv run alembic upgrade head

# 4. Load sample data (optional)
uv run load-sample

# 5. Start CLI
uv run oee-tracker
```

## Database

### Tables:

Name: machines
Columns: id, name, ideal_cycle_time, location

Name: reason_codes
Columns: code, is_planned, description

Name: shifts
Columns: id, name

Name: operators
Columns: id, name

Name: production_runs
Columns: id, machine_id, shift_id, operator_id, planned_start_time, planned_end_time, actual_start_time, actual_end_time, good_parts, rejected_parts

Name: downtime_events
Columns: id, production_run_id, reason_code, start_time, end_time

## Usage

```bash
oee-tracker --help
```

## OEE Formula

- **Availability** = Run Time / Planned Production Time
- **Performance** = (Ideal Cycle Time × Total Parts) / Run Time
- **Quality** = Good Parts / Total Parts
- **OEE** = Availability × Performance × Quality