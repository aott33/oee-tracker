# cli/report.py
import typer
from typing import Annotated
from datetime import datetime

import oee_tracker.crud as crud
import oee_tracker.db as db

app = typer.Typer(help="OEE calculations and reports.")


def parse_date(date_str: str | None) -> datetime | None:
    """Parse date string to datetime."""
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid date format '{date_str}'. Use YYYY-MM-DD")
        raise typer.Exit(code=1)


def format_percent(value: float) -> str:
    """Format float as percentage."""
    return f"{value * 100:.1f}%"


# ============================================================
# OEE CALCULATIONS
# ============================================================

@app.command()
def oee(run_id: int):
    """Calculate OEE for a single production run."""

    session = db.get_session()

    try:
        result = crud.calculate_oee(session, run_id)

        if result is None:
            print(f"Error: Cannot calculate OEE for run {run_id}")
            print("  Run may not exist, be incomplete, or missing part counts.")
            raise typer.Exit(code=1)

        print(f"OEE Report for Production Run {run_id}")
        print(f"  Availability: {format_percent(result['availability'])}")
        print(f"  Performance:  {format_percent(result['performance'])}")
        print(f"  Quality:      {format_percent(result['quality'])}")
        print(f"  ─────────────────────")
        print(f"  OEE:          {format_percent(result['oee'])}")

    finally:
        session.close()


@app.command()
def machine(
    machine_id: int,
    start: Annotated[str, typer.Option(help="Start date (YYYY-MM-DD)")] = None,
    end: Annotated[str, typer.Option(help="End date (YYYY-MM-DD)")] = None,
):
    """Calculate OEE for a machine over a date range."""

    session = db.get_session()

    try:
        start_date = parse_date(start)
        end_date = parse_date(end)

        result = crud.calculate_oee_by_machine(session, machine_id, start_date, end_date)

        if result is None:
            print(f"Error: No completed runs found for machine {machine_id}")
            raise typer.Exit(code=1)

        # Get machine name
        machine_obj = crud.get_machine(session, machine_id)
        machine_name = machine_obj.name if machine_obj else f"Machine {machine_id}"

        print(f"OEE Report for {machine_name}")
        if start_date or end_date:
            date_range = f"{start or 'beginning'} to {end or 'now'}"
            print(f"  Date Range: {date_range}")
        print(f"  Runs: {result['runs_included']}/{result['runs_total']} included")
        print()
        print(f"  Avg Availability: {format_percent(result['avg_availability'])}")
        print(f"  Avg Performance:  {format_percent(result['avg_performance'])}")
        print(f"  Avg Quality:      {format_percent(result['avg_quality'])}")
        print(f"  ─────────────────────────")
        print(f"  Avg OEE:          {format_percent(result['avg_oee'])}")

    finally:
        session.close()


@app.command()
def shift(
    shift_id: int,
    start: Annotated[str, typer.Option(help="Start date (YYYY-MM-DD)")] = None,
    end: Annotated[str, typer.Option(help="End date (YYYY-MM-DD)")] = None,
):
    """Calculate OEE for a shift over a date range."""

    session = db.get_session()

    try:
        start_date = parse_date(start)
        end_date = parse_date(end)

        result = crud.calculate_oee_by_shift(session, shift_id, start_date, end_date)

        if result is None:
            print(f"Error: No completed runs found for shift {shift_id}")
            raise typer.Exit(code=1)

        # Get shift name
        shift_obj = crud.get_shift(session, shift_id)
        shift_name = shift_obj.name if shift_obj else f"Shift {shift_id}"

        print(f"OEE Report for {shift_name}")
        if start_date or end_date:
            date_range = f"{start or 'beginning'} to {end or 'now'}"
            print(f"  Date Range: {date_range}")
        print(f"  Runs: {result['runs_included']}/{result['runs_total']} included")
        print()
        print(f"  Avg Availability: {format_percent(result['avg_availability'])}")
        print(f"  Avg Performance:  {format_percent(result['avg_performance'])}")
        print(f"  Avg Quality:      {format_percent(result['avg_quality'])}")
        print(f"  ─────────────────────────")
        print(f"  Avg OEE:          {format_percent(result['avg_oee'])}")

    finally:
        session.close()


# ============================================================
# REPORTS
# ============================================================

@app.command()
def downtime(
    limit: Annotated[int, typer.Option(help="Number of top reasons to show")] = 5,
    start: Annotated[str, typer.Option(help="Start date (YYYY-MM-DD)")] = None,
    end: Annotated[str, typer.Option(help="End date (YYYY-MM-DD)")] = None,
):
    """Show top downtime reasons by total duration."""

    session = db.get_session()

    try:
        start_date = parse_date(start)
        end_date = parse_date(end)

        results = crud.get_top_downtime_reasons(session, limit, start_date, end_date)

        if not results:
            print("No downtime data found.")
            return

        print(f"Top {len(results)} Downtime Reasons")
        if start_date or end_date:
            date_range = f"{start or 'beginning'} to {end or 'now'}"
            print(f"Date Range: {date_range}")
        print()
        print(f"{'Rank':<6}{'Code':<12}{'Description':<30}{'Minutes':<10}")
        print("─" * 58)

        for i, reason in enumerate(results, 1):
            minutes = reason['total_duration_minutes']
            if minutes is not None:
                minutes_str = f"{minutes:.1f}"
            else:
                minutes_str = "N/A"
            print(f"{i:<6}{reason['reason_code']:<12}{reason['description']:<30}{minutes_str:<10}")

    finally:
        session.close()


@app.command()
def machines(
    start: Annotated[str, typer.Option(help="Start date (YYYY-MM-DD)")] = None,
    end: Annotated[str, typer.Option(help="End date (YYYY-MM-DD)")] = None,
):
    """Rank all machines by OEE."""

    session = db.get_session()

    try:
        start_date = parse_date(start)
        end_date = parse_date(end)

        results = crud.get_machines_ranked_by_oee(session, start_date, end_date)

        if not results:
            print("No OEE data found for any machines.")
            return

        print("Machines Ranked by OEE")
        if start_date or end_date:
            date_range = f"{start or 'beginning'} to {end or 'now'}"
            print(f"Date Range: {date_range}")
        print()
        print(f"{'Rank':<6}{'Machine':<12}{'OEE':<10}{'Avail':<10}{'Perf':<10}{'Quality':<10}{'Runs':<8}")
        print("─" * 66)

        for i, m in enumerate(results, 1):
            # Get machine name
            machine_obj = crud.get_machine(session, m['machine_id'])
            name = machine_obj.name if machine_obj else f"ID:{m['machine_id']}"

            print(f"{i:<6}{name:<12}{format_percent(m['avg_oee']):<10}{format_percent(m['avg_availability']):<10}{format_percent(m['avg_performance']):<10}{format_percent(m['avg_quality']):<10}{m['runs_included']:<8}")

    finally:
        session.close()


@app.command()
def shifts(
    start: Annotated[str, typer.Option(help="Start date (YYYY-MM-DD)")] = None,
    end: Annotated[str, typer.Option(help="End date (YYYY-MM-DD)")] = None,
):
    """Compare all shifts by OEE."""

    session = db.get_session()

    try:
        start_date = parse_date(start)
        end_date = parse_date(end)

        results = crud.compare_shifts(session, start_date, end_date)

        if not results:
            print("No OEE data found for any shifts.")
            return

        print("Shifts Comparison by OEE")
        if start_date or end_date:
            date_range = f"{start or 'beginning'} to {end or 'now'}"
            print(f"Date Range: {date_range}")
        print()
        print(f"{'Rank':<6}{'Shift':<15}{'OEE':<10}{'Avail':<10}{'Perf':<10}{'Quality':<10}{'Runs':<8}")
        print("─" * 69)

        for i, s in enumerate(results, 1):
            # Get shift name
            shift_obj = crud.get_shift(session, s['shift_id'])
            name = shift_obj.name if shift_obj else f"ID:{s['shift_id']}"

            print(f"{i:<6}{name:<15}{format_percent(s['avg_oee']):<10}{format_percent(s['avg_availability']):<10}{format_percent(s['avg_performance']):<10}{format_percent(s['avg_quality']):<10}{s['runs_included']:<8}")

    finally:
        session.close()
