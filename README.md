# Production Line OEE Tracker

Track Overall Equipment Effectiveness across CNC machines and shifts.

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Database

```bash
alembic upgrade head
```

## Usage

```bash
oee-tracker --help
```

## OEE Formula

- **Availability** = Run Time / Planned Production Time
- **Performance** = (Ideal Cycle Time × Total Parts) / Run Time
- **Quality** = Good Parts / Total Parts
- **OEE** = Availability × Performance × Quality