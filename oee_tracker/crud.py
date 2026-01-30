"""
CRUD operations and queries for OEE Tracker.
"""

from datetime import datetime
from sqlalchemy.orm import Session

from oee_tracker.models import (
    Machine,
    Shift,
    Operator,
    ReasonCode,
    ProductionRun,
    DowntimeEvent,
)


# ============================================================
# MACHINES
# ============================================================

def create_machine(
    session: Session,
    name: str,
    ideal_cycle_time: float,
    location: str | None = None,
) -> Machine:
    """Create a new machine."""
    pass


def get_machine(session: Session, machine_id: int) -> Machine | None:
    """Get a machine by ID."""
    pass


def get_all_machines(session: Session) -> list[Machine]:
    """Get all machines."""
    pass


def update_machine(
    session: Session,
    machine_id: int,
    name: str | None = None,
    ideal_cycle_time: float | None = None,
    location: str | None = None,
) -> Machine | None:
    """Update a machine. Returns None if not found."""
    pass


def delete_machine(session: Session, machine_id: int, is_admin: bool = False) -> bool:
    """Delete a machine. Returns True if deleted, False if not found or unauthorized."""
    pass


# ============================================================
# SHIFTS
# ============================================================

def create_shift(session: Session, name: str) -> Shift:
    """Create a new shift."""
    pass


def get_shift(session: Session, shift_id: int) -> Shift | None:
    """Get a shift by ID."""
    pass


def get_all_shifts(session: Session) -> list[Shift]:
    """Get all shifts."""
    pass


def update_shift(session: Session, shift_id: int, name: str) -> Shift | None:
    """Update a shift. Returns None if not found."""
    pass


def delete_shift(session: Session, shift_id: int, is_admin: bool = False) -> bool:
    """Delete a shift. Returns True if deleted, False if not found or unauthorized."""
    pass


# ============================================================
# OPERATORS
# ============================================================

def create_operator(session: Session, name: str) -> Operator:
    """Create a new operator."""
    pass


def get_operator(session: Session, operator_id: int) -> Operator | None:
    """Get an operator by ID."""
    pass


def get_all_operators(session: Session) -> list[Operator]:
    """Get all operators."""
    pass


def update_operator(session: Session, operator_id: int, name: str) -> Operator | None:
    """Update an operator. Returns None if not found."""
    pass


def delete_operator(session: Session, operator_id: int, is_admin: bool = False) -> bool:
    """Delete an operator. Returns True if deleted, False if not found or unauthorized."""
    pass


# ============================================================
# REASON CODES
# ============================================================

def create_reason_code(
    session: Session,
    code: str,
    description: str,
    is_planned: bool = False,
) -> ReasonCode:
    """Create a new reason code."""
    pass


def get_reason_code(session: Session, code: str) -> ReasonCode | None:
    """Get a reason code by code."""
    pass


def get_all_reason_codes(session: Session) -> list[ReasonCode]:
    """Get all reason codes."""
    pass


def get_planned_reason_codes(session: Session) -> list[ReasonCode]:
    """Get all planned reason codes."""
    pass


def get_unplanned_reason_codes(session: Session) -> list[ReasonCode]:
    """Get all unplanned reason codes."""
    pass


def update_reason_code(
    session: Session,
    code: str,
    description: str | None = None,
    is_planned: bool | None = None,
) -> ReasonCode | None:
    """Update a reason code. Returns None if not found."""
    pass


def delete_reason_code(session: Session, code: str, is_admin: bool = False) -> bool:
    """Delete a reason code. Returns True if deleted, False if not found or unauthorized."""
    pass


# ============================================================
# PRODUCTION RUNS
# ============================================================

def create_production_run(
    session: Session,
    machine_id: int,
    shift_id: int,
    operator_id: int,
    planned_start_time: datetime,
    planned_end_time: datetime,
) -> ProductionRun:
    """Create a new production run (scheduled, not yet started)."""
    pass


def get_production_run(session: Session, run_id: int) -> ProductionRun | None:
    """Get a production run by ID."""
    pass


def get_all_production_runs(session: Session) -> list[ProductionRun]:
    """Get all production runs."""
    pass


def get_production_runs_by_machine(
    session: Session,
    machine_id: int,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[ProductionRun]:
    """Get production runs for a machine, optionally filtered by date range."""
    pass


def get_production_runs_by_shift(
    session: Session,
    shift_id: int,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[ProductionRun]:
    """Get production runs for a shift, optionally filtered by date range."""
    pass


def get_active_production_runs(session: Session) -> list[ProductionRun]:
    """Get all currently running production runs (started but not ended)."""
    pass


def start_run(session: Session, run_id: int) -> ProductionRun | None:
    """Start a production run. Sets actual_start_time to now. Returns None if not found."""
    pass


def stop_run(
    session: Session,
    run_id: int,
    good_parts_count: int,
    rejected_parts_count: int,
) -> ProductionRun | None:
    """Stop a production run. Sets actual_end_time to now and part counts. Returns None if not found."""
    pass


def update_production_run(
    session: Session,
    run_id: int,
    good_parts_count: int | None = None,
    rejected_parts_count: int | None = None,
) -> ProductionRun | None:
    """Update part counts on a production run. Returns None if not found."""
    pass


def delete_production_run(session: Session, run_id: int, is_admin: bool = False) -> bool:
    """Delete a production run. Returns True if deleted, False if not found or unauthorized."""
    pass


# ============================================================
# DOWNTIME EVENTS
# ============================================================

def create_downtime_event(
    session: Session,
    production_run_id: int,
    reason_code: str,
    start_time: datetime,
    end_time: datetime | None = None,
) -> DowntimeEvent:
    """Create a downtime event with explicit times."""
    pass


def get_downtime_event(session: Session, event_id: int) -> DowntimeEvent | None:
    """Get a downtime event by ID."""
    pass


def get_downtime_events_by_run(session: Session, run_id: int) -> list[DowntimeEvent]:
    """Get all downtime events for a production run."""
    pass


def get_active_downtime_events(session: Session) -> list[DowntimeEvent]:
    """Get all currently active downtime events (started but not ended)."""
    pass


def start_downtime(
    session: Session,
    production_run_id: int,
    reason_code: str,
) -> DowntimeEvent:
    """Start a downtime event. Sets start_time to now."""
    pass


def stop_downtime(session: Session, event_id: int) -> DowntimeEvent | None:
    """Stop a downtime event. Sets end_time to now. Returns None if not found."""
    pass


def delete_downtime_event(session: Session, event_id: int, is_admin: bool = False) -> bool:
    """Delete a downtime event. Returns True if deleted, False if not found or unauthorized."""
    pass


# ============================================================
# OEE CALCULATIONS
# ============================================================

def calculate_availability(
    session: Session,
    run_id: int,
) -> float | None:
    """
    Calculate availability for a production run.
    Availability = Run Time / Planned Production Time
    Returns None if run not found or incomplete.
    """
    pass


def calculate_performance(
    session: Session,
    run_id: int,
) -> float | None:
    """
    Calculate performance for a production run.
    Performance = (Ideal Cycle Time × Total Parts) / Run Time
    Returns None if run not found or incomplete.
    """
    pass


def calculate_quality(
    session: Session,
    run_id: int,
) -> float | None:
    """
    Calculate quality for a production run.
    Quality = Good Parts / Total Parts
    Returns None if run not found or incomplete.
    """
    pass


def calculate_oee(
    session: Session,
    run_id: int,
) -> dict | None:
    """
    Calculate OEE for a production run.
    Returns dict with availability, performance, quality, and oee.
    Returns None if run not found or incomplete.
    """
    pass


def calculate_oee_by_machine(
    session: Session,
    machine_id: int,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> dict | None:
    """Calculate aggregate OEE for a machine over a date range."""
    pass


def calculate_oee_by_shift(
    session: Session,
    shift_id: int,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> dict | None:
    """Calculate aggregate OEE for a shift over a date range."""
    pass


# ============================================================
# REPORTS
# ============================================================

def get_top_downtime_reasons(
    session: Session,
    limit: int = 3,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[dict]:
    """
    Get top downtime reasons by total duration.
    Returns list of dicts with reason_code, description, total_duration_minutes.
    """
    pass


def get_machines_ranked_by_oee(
    session: Session,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[dict]:
    """
    Get machines ranked by OEE.
    Returns list of dicts with machine_id, name, oee.
    """
    pass


def compare_shifts(
    session: Session,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[dict]:
    """
    Compare shift performance.
    Returns list of dicts with shift_id, name, availability, performance, quality, oee.
    """
    pass