# cli/machine.py
import typer

app = typer.Typer()

@app.command()
def list():
    """List all machines."""
    print("here are the machines")