# Production Line OEE Tracker

Track Overall Equipment Effectiveness across CNC machines and shifts.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Database

```bash
alembic upgrade head
```

## Usage

```bash
python -m oee_tracker.cli --help
```

## OEE Formula

- **Availability** = Run Time / Planned Production Time
- **Performance** = (Ideal Cycle Time × Total Parts) / Run Time
- **Quality** = Good Parts / Total Parts
- **OEE** = Availability × Performance × Quality
