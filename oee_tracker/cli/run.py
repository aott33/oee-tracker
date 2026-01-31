# cli/run.py
import typer
from typing import Annotated
from datetime import datetime

import oee_tracker.crud as crud
import oee_tracker.db as db

app = typer.Typer(help="Manage production runs.")


@app.command()
def create(
    machine_id: int,
    shift_id: int,
    operator_id: int,
    planned_start: Annotated[str, typer.Argument(help="Planned start time (YYYY-MM-DD HH:MM:SS)")],
    planned_end: Annotated[str, typer.Argument(help="Planned end time (YYYY-MM-DD HH:MM:SS)")],
):
    """Create new production run."""

    session = db.get_session()

    try:
        planned_start_time = datetime.strptime(planned_start, "%Y-%m-%d %H:%M:%S")
        planned_end_time = datetime.strptime(planned_end, "%Y-%m-%d %H:%M:%S")

        run = crud.create_production_run(
            session,
            machine_id,
            shift_id,
            operator_id,
            planned_start_time,
            planned_end_time,
        )

        if run is None:
            raise typer.Exit(code=1)

        print(f"Production run created: {run.id}")
        print(f"  Machine: {run.machine_id}, Shift: {run.shift_id}, Operator: {run.operator_id}")
        print(f"  Planned: {run.planned_start_time} - {run.planned_end_time}")

    except ValueError:
        print("Error: Invalid datetime format. Use YYYY-MM-DD HH:MM:SS")
        raise typer.Exit(code=1)

    finally:
        session.close()


@app.command()
def list():
    """List all production runs."""

    session = db.get_session()

    try:
        runs = crud.get_all_production_runs(session)

        if not runs:
            print("No production runs found.")
            return

        for run in runs:
            status = "Pending"
            if run.actual_start_time and not run.actual_end_time:
                status = "Running"
            elif run.actual_end_time:
                status = "Completed"

            print(f"{run.id}: Machine {run.machine_id} | Shift {run.shift_id} | {status}")

    finally:
        session.close()


@app.command()
def get(run_id: int):
    """Get production run by id."""

    session = db.get_session()

    try:
        run = crud.get_production_run(session, run_id)

        if run is None:
            print(f"Error: Production run {run_id} not found")
            raise typer.Exit(code=1)

        status = "Pending"
        if run.actual_start_time and not run.actual_end_time:
            status = "Running"
        elif run.actual_end_time:
            status = "Completed"

        print(f"Production Run {run.id} ({status})")
        print(f"  Machine: {run.machine_id}, Shift: {run.shift_id}, Operator: {run.operator_id}")
        print(f"  Planned: {run.planned_start_time} - {run.planned_end_time}")
        if run.actual_start_time:
            print(f"  Actual Start: {run.actual_start_time}")
        if run.actual_end_time:
            print(f"  Actual End: {run.actual_end_time}")
        if run.good_parts_count is not None:
            print(f"  Good Parts: {run.good_parts_count}, Rejected: {run.rejected_parts_count}")

    finally:
        session.close()


@app.command()
def active():
    """List active (running) production runs."""

    session = db.get_session()

    try:
        runs = crud.get_active_production_runs(session)

        if not runs:
            print("No active production runs.")
            return

        print("Active Production Runs:")
        for run in runs:
            print(f"  {run.id}: Machine {run.machine_id} | Started: {run.actual_start_time}")

    finally:
        session.close()


@app.command()
def start(run_id: int):
    """Start a production run."""
    session = db.get_session()

    try:
        run = crud.start_run(session, run_id)

        if run is None:
            print(f"Error: Production run {run_id} not found")
            raise typer.Exit(code=1)

        print(f"Production run {run_id} started")

    finally:
        session.close()


@app.command()
def stop(
    run_id: int,
    good_parts: Annotated[int, typer.Argument(help="Number of good parts produced")],
    rejected_parts: Annotated[int, typer.Argument(help="Number of rejected parts")],
):
    """Stop a production run with part counts."""
    session = db.get_session()

    try:
        run = crud.stop_run(session, run_id, good_parts, rejected_parts)

        if run is None:
            print(f"Error: Production run {run_id} not found")
            raise typer.Exit(code=1)

        print(f"Production run {run_id} stopped")
        print(f"  Good parts: {good_parts}, Rejected: {rejected_parts}")

    finally:
        session.close()


@app.command()
def update(
    run_id: int,
    good_parts: Annotated[int, typer.Option(help="Update good parts count")] = None,
    rejected_parts: Annotated[int, typer.Option(help="Update rejected parts count")] = None,
):
    """Update production run part counts."""
    session = db.get_session()

    try:
        run = crud.update_production_run(session, run_id, good_parts, rejected_parts)

        if run is None:
            print(f"Error: Production run {run_id} not found")
            raise typer.Exit(code=1)

        print(f"Production run {run_id} updated")
        print(f"  Good parts: {run.good_parts_count}, Rejected: {run.rejected_parts_count}")

    finally:
        session.close()


@app.command()
def delete(run_id: int):
    """Delete production run."""
    session = db.get_session()

    try:
        deleted = crud.delete_production_run(session, run_id)

        if deleted:
            print(f"Production run {run_id} deleted")
        else:
            print(f"Production run {run_id} not found")

    finally:
        session.close()
