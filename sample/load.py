"""
Sample data loader for OEE Tracker

Usage:
    uv run load-sample

Loads CSV files from sample/data/ into the database.
"""

import csv
from datetime import datetime
from pathlib import Path
from sqlalchemy import text

from oee_tracker.db import get_session
from oee_tracker.models import Machine, Shift, Operator, ReasonCode, ProductionRun

SAMPLE_DATA_DIR = Path(__file__).parent / "data"


def load_csv(filename: str) -> list[dict]:
    """Load a CSV file and return list of dicts."""
    filepath = SAMPLE_DATA_DIR / filename
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def parse_bool(value: str) -> bool:
    """Parse boolean from CSV string."""
    return value.lower() == "true"


def parse_datetime(value: str) -> datetime:
    """Parse datetime from CSV string."""
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def main():
    session = get_session()

    try:
        # Load machines
        for row in load_csv("machines.csv"):
            machine = Machine(
                id=int(row["id"]),
                name=row["name"],
                ideal_cycle_time=float(row["ideal_cycle_time"]),
                location=row["location"],
            )
            session.add(machine)
        print("Loaded machines")

        # Load shifts
        for row in load_csv("shifts.csv"):
            shift = Shift(
                id=int(row["id"]),
                name=row["name"],
            )
            session.add(shift)
        print("Loaded shifts")

        # Load operators
        for row in load_csv("operators.csv"):
            operator = Operator(
                id=int(row["id"]),
                name=row["name"],
            )
            session.add(operator)
        print("Loaded operators")

        # Load reason codes
        for row in load_csv("reason_codes.csv"):
            reason_code = ReasonCode(
                code=row["code"],
                description=row["description"],
                is_planned=parse_bool(row["is_planned"]),
            )
            session.add(reason_code)
        print("Loaded reason codes")

        # Load production runs
        for row in load_csv("production_runs.csv"):
            production_run = ProductionRun(
                id=int(row["id"]),
                machine_id=int(row["machine_id"]),
                shift_id=int(row["shift_id"]),
                operator_id=int(row["operator_id"]),
                planned_start_time=parse_datetime(row["planned_start_time"]),
                planned_end_time=parse_datetime(row["planned_end_time"]),
                actual_start_time=parse_datetime(row["actual_start_time"]),
                actual_end_time=parse_datetime(row["actual_end_time"]),
                good_parts_count=int(row["good_parts_count"]),
                rejected_parts_count=int(row["rejected_parts_count"]),
            )
            session.add(production_run)
        print("Loaded production runs")

        # Skipping downtime_events as requested

        session.commit()

        # Reset sequences after loading sample data with explicit IDs
        session.execute(text("SELECT setval('machines_id_seq', (SELECT MAX(id) FROM machines))"))
        session.execute(text("SELECT setval('shifts_id_seq', (SELECT MAX(id) FROM shifts))"))
        session.execute(text("SELECT setval('operators_id_seq', (SELECT MAX(id) FROM operators))"))
        session.execute(text("SELECT setval('production_runs_id_seq', (SELECT MAX(id) FROM production_runs))"))
        session.commit()
        print("Reset ID sequences")

        print("Done!")

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


if __name__ == "__main__":
    main()