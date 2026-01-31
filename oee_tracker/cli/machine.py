# cli/machine.py
import typer
from typing import Annotated

import oee_tracker.crud as crud
import oee_tracker.db as db

app = typer.Typer()

@app.command()
def create(
    name: str,
    ideal_cycle_time: float,
    loc: Annotated[str, typer.Option(help="Add machine location")] = None,
):
    """Create new machine."""
    
    session = db.get_session()

    try:
        machine = crud.create_machine(
            session,
            name,
            ideal_cycle_time,
            loc
        )

        if machine is None:
            raise typer.Exit(code=1)

        if machine:
            msg = f"Machine created: {machine.name} - {machine.ideal_cycle_time}s"
            if machine.location:
                msg = f"Machine created: {machine.name} - {machine.location} - {machine.ideal_cycle_time}s"
        print(msg)
    
    finally:
        session.close()

@app.command()
def list():
    """List all machines."""
    
    session = db.get_session()

    try:
        print("CNC Machines")

        machines = crud.get_all_machines(session)

        if machines is None:
            print("No machines found.")
            return
        
        for machine in machines:
            if machine.location is not None:
                print(f"{machine.id}: {machine.name} - {machine.location} - {machine.ideal_cycle_time}s")
            elif machine.location is None:
                print(f"{machine.id}: {machine.name} - {machine.ideal_cycle_time}s")

    finally:
        session.close()