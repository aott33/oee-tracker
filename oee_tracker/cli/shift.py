# cli/shift.py
import typer
from typing import Annotated

import oee_tracker.crud as crud
import oee_tracker.db as db

app = typer.Typer(help="Manage shifts.")


@app.command()
def create(name: str):
    """Create new shift."""

    session = db.get_session()

    try:
        shift = crud.create_shift(session, name)

        if shift is None:
            raise typer.Exit(code=1)

        print(f"Shift created: {shift.id}: {shift.name}")

    finally:
        session.close()


@app.command()
def list():
    """List all shifts."""

    session = db.get_session()

    try:
        shifts = crud.get_all_shifts(session)

        if not shifts:
            print("No shifts found.")
            return

        for shift in shifts:
            print(f"{shift.id}: {shift.name}")

    finally:
        session.close()


@app.command()
def get(shift_id: int):
    """Get shift by id."""

    session = db.get_session()

    try:
        shift = crud.get_shift(session, shift_id)

        if shift is None:
            print(f"Error: Shift {shift_id} not found")
            raise typer.Exit(code=1)

        print(f"{shift.id}: {shift.name}")

    finally:
        session.close()


@app.command()
def update(
    shift_id: int,
    name: Annotated[str, typer.Option(help="Update shift name")] = None,
):
    """Update shift information."""
    session = db.get_session()

    try:
        shift = crud.update_shift(session, shift_id, name)

        if shift is None:
            print(f"Error: Shift {shift_id} not found")
            raise typer.Exit(code=1)

        print(f"Shift updated: {shift.id}: {shift.name}")

    finally:
        session.close()


@app.command()
def delete(shift_id: int):
    """Delete shift."""
    session = db.get_session()

    try:
        deleted = crud.delete_shift(session, shift_id)

        if deleted:
            print(f"Shift {shift_id} deleted")
        else:
            print(f"Shift {shift_id} not found")

    finally:
        session.close()
