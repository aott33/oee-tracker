# CLI Package
import typer
from oee_tracker.cli import machine, shift, operator, run, downtime, report

app = typer.Typer(help="An awesome OEE CLI Tool.")

app.add_typer(machine.app, name="machine")
app.add_typer(shift.app, name="shift")
app.add_typer(operator.app, name="operator")
app.add_typer(run.app, name="run")
app.add_typer(downtime.app, name="downtime")
app.add_typer(report.app, name="report")

def main():
    app()