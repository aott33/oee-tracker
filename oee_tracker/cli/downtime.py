# cli/downtime.py
import typer
from typing import Annotated

import oee_tracker.crud as crud
import oee_tracker.db as db

app = typer.Typer(help="Manage downtime events.")


@app.command()
def create(
    run_id: int,
    reason_code: str,
):
    """Create new downtime event (starts now)."""

    session = db.get_session()

    try:
        event = crud.create_downtime_event(session, run_id, reason_code)

        if event is None:
            raise typer.Exit(code=1)

        print(f"Downtime event created: {event.id}")
        print(f"  Run: {event.production_run_id}, Reason: {event.reason_code}")
        print(f"  Started: {event.start_time}")

    finally:
        session.close()


@app.command()
def list(
    run_id: Annotated[int, typer.Option(help="Filter by production run ID")] = None,
):
    """List downtime events."""

    session = db.get_session()

    try:
        if run_id:
            events = crud.get_downtime_events_by_run(session, run_id)
        else:
            # Get all - we need to add this to crud, for now use active
            events = crud.get_active_downtime_events(session)
            if not events:
                print("No active downtime events. Use --run-id to filter by run.")
                return

        if not events:
            print("No downtime events found.")
            return

        for event in events:
            status = "Active" if event.end_time is None else "Ended"
            print(f"{event.id}: Run {event.production_run_id} | {event.reason_code} | {status}")

    finally:
        session.close()


@app.command()
def get(event_id: int):
    """Get downtime event by id."""

    session = db.get_session()

    try:
        event = crud.get_downtime_event(session, event_id)

        if event is None:
            print(f"Error: Downtime event {event_id} not found")
            raise typer.Exit(code=1)

        status = "Active" if event.end_time is None else "Ended"
        print(f"Downtime Event {event.id} ({status})")
        print(f"  Run: {event.production_run_id}")
        print(f"  Reason: {event.reason_code}")
        print(f"  Start: {event.start_time}")
        if event.end_time:
            print(f"  End: {event.end_time}")

    finally:
        session.close()


@app.command()
def active():
    """List active (ongoing) downtime events."""

    session = db.get_session()

    try:
        events = crud.get_active_downtime_events(session)

        if not events:
            print("No active downtime events.")
            return

        print("Active Downtime Events:")
        for event in events:
            print(f"  {event.id}: Run {event.production_run_id} | {event.reason_code} | Started: {event.start_time}")

    finally:
        session.close()


@app.command()
def stop(event_id: int):
    """Stop a downtime event (ends now)."""
    session = db.get_session()

    try:
        event = crud.stop_downtime(session, event_id)

        if event is None:
            print(f"Error: Downtime event {event_id} not found")
            raise typer.Exit(code=1)

        print(f"Downtime event {event_id} stopped")

    finally:
        session.close()


@app.command()
def delete(event_id: int):
    """Delete downtime event."""
    session = db.get_session()

    try:
        deleted = crud.delete_downtime_event(session, event_id)

        if deleted:
            print(f"Downtime event {event_id} deleted")
        else:
            print(f"Downtime event {event_id} not found")

    finally:
        session.close()
