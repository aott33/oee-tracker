# cli/operator.py
import typer
from typing import Annotated

import oee_tracker.crud as crud
import oee_tracker.db as db

app = typer.Typer(help="Manage operators.")


@app.command()
def create(name: str):
    """Create new operator."""

    session = db.get_session()

    try:
        operator = crud.create_operator(session, name)

        if operator is None:
            raise typer.Exit(code=1)

        print(f"Operator created: {operator.id}: {operator.name}")

    finally:
        session.close()


@app.command()
def list():
    """List all operators."""

    session = db.get_session()

    try:
        operators = crud.get_all_operators(session)

        if not operators:
            print("No operators found.")
            return

        for operator in operators:
            print(f"{operator.id}: {operator.name}")

    finally:
        session.close()


@app.command()
def get(operator_id: int):
    """Get operator by id."""

    session = db.get_session()

    try:
        operator = crud.get_operator(session, operator_id)

        if operator is None:
            print(f"Error: Operator {operator_id} not found")
            raise typer.Exit(code=1)

        print(f"{operator.id}: {operator.name}")

    finally:
        session.close()


@app.command()
def update(
    operator_id: int,
    name: Annotated[str, typer.Option(help="Update operator name")] = None,
):
    """Update operator information."""
    session = db.get_session()

    try:
        operator = crud.update_operator(session, operator_id, name)

        if operator is None:
            print(f"Error: Operator {operator_id} not found")
            raise typer.Exit(code=1)

        print(f"Operator updated: {operator.id}: {operator.name}")

    finally:
        session.close()


@app.command()
def delete(operator_id: int):
    """Delete operator."""
    session = db.get_session()

    try:
        deleted = crud.delete_operator(session, operator_id)

        if deleted:
            print(f"Operator {operator_id} deleted")
        else:
            print(f"Operator {operator_id} not found")

    finally:
        session.close()
