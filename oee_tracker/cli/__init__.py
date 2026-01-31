# CLI Package
import typer
from oee_tracker.cli import machine

app = typer.Typer(help="An awesome OEE CLI Tool.")

app.add_typer(machine.app, name="machine")

def main():
    app()