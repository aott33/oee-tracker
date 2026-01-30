"""
CRUD operations and queries for OEE Tracker.
"""

from datetime import datetime
from sqlalchemy import (
    select,
    func,
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
    OperationalError,
    DataError,
) 

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
) -> Machine | None:
    """Create a new machine."""
    machine = Machine(name=name, ideal_cycle_time=ideal_cycle_time, location=location)
    try:
        session.add(machine)
        session.commit()
        return machine
    except IntegrityError:
        session.rollback()
        print("Error: Machine already exists")
        return None
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None


def get_machine(session: Session, machine_id: int) -> Machine | None:
    """Get a machine by ID."""
    try:
        machine = session.get(Machine, machine_id)
        return machine
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None


def get_all_machines(session: Session) -> list[Machine]:
    """Get all machines."""
    try:
        machines = session.scalars(select(Machine))
        return list(machines)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []

def update_machine(
    session: Session,
    machine_id: int,
    name: str | None = None,
    ideal_cycle_time: float | None = None,
    location: str | None = None,
) -> Machine | None:
    """Update a machine. Returns None if not found."""
    try:
        machine = session.get(Machine, machine_id)
        if machine:
            if name is not None:
                machine.name = name
            if ideal_cycle_time is not None:
                machine.ideal_cycle_time = ideal_cycle_time
            if location is not None:
                machine.location = location
            session.commit()

        return machine
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None

def delete_machine(session: Session, machine_id: int, is_admin: bool = False) -> bool:
    """Delete a machine. Returns True if deleted, False if not found or unauthorized."""
    try:
        machine = session.get(Machine, machine_id)
        if machine:
            session.delete(machine)
            session.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return False


# ============================================================
# SHIFTS
# ============================================================

def create_shift(session: Session, name: str) -> Shift | None:
    """Create a new shift."""
    shift = Shift(name=name)
    try:
        session.add(shift)
        session.commit()
        return shift
    except IntegrityError:
        session.rollback()
        print("Error: Shift already exists")
        return None
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None


def get_shift(session: Session, shift_id: int) -> Shift | None:
    """Get a shift by ID."""
    try:
        shift = session.get(Shift, shift_id)
        return shift
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None


def get_all_shifts(session: Session) -> list[Shift]:
    """Get all shifts."""
    try:
        shifts = session.scalars(select(Shift))
        return list(shifts)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []


def update_shift(session: Session, shift_id: int, name: str) -> Shift | None:
    """Update a shift. Returns None if not found."""
    try:
        shift = session.get(Shift, shift_id)
        if shift is not None:
            shift.name = name
            session.commit()
        return shift
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None


def delete_shift(session: Session, shift_id: int, is_admin: bool = False) -> bool:
    """Delete a shift. Returns True if deleted, False if not found or unauthorized."""
    try:
        shift = session.get(Shift, shift_id)
        if shift is not None:
            session.delete(shift)
            session.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return False


# ============================================================
# OPERATORS
# ============================================================

def create_operator(session: Session, name: str) -> Operator | None:
    """Create a new operator."""
    operator = Operator(name=name)
    try:
        session.add(operator)
        session.commit()
        return operator
    except IntegrityError:
        session.rollback()
        print("Error: Operator already exists")
        return None
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None


def get_operator(session: Session, operator_id: int) -> Operator | None:
    """Get an operator by ID."""
    try:
        operator = session.get(Operator, operator_id)
        return operator
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None


def get_all_operators(session: Session) -> list[Operator]:
    """Get all operators."""
    try:
        operators = session.scalars(select(Operator))
        return list(operators)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []


def update_operator(session: Session, operator_id: int, name: str) -> Operator | None:
    """Update an operator. Returns None if not found."""
    try:
        operator = session.get(Operator, operator_id)
        if operator is not None:
            operator.name = name
            session.commit()
        return operator
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None


def delete_operator(session: Session, operator_id: int, is_admin: bool = False) -> bool:
    """Delete an operator. Returns True if deleted, False if not found or unauthorized."""
    try:
        operator = session.get(Operator, operator_id)
        if operator is not None:
            session.delete(operator)
            session.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return False


# ============================================================
# REASON CODES
# ============================================================

def create_reason_code(
    session: Session,
    code: str,
    description: str,
    is_planned: bool = False,
) -> ReasonCode | None:
    """Create a new reason code."""
    reason_code = ReasonCode(code=code, description=description, is_planned=is_planned)
    try:
        session.add(reason_code)
        session.commit()
        return reason_code
    except IntegrityError:
        session.rollback()
        print("Error: Reason code already exists")
        return None
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None


def get_reason_code(session: Session, code: str) -> ReasonCode | None:
    """Get a reason code by code."""
    try:
        reason_code = session.get(ReasonCode, code)
        return reason_code
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None


def get_all_reason_codes(session: Session) -> list[ReasonCode]:
    """Get all reason codes."""
    try:
        reason_codes = session.scalars(select(ReasonCode))
        return list(reason_codes)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []


def get_planned_reason_codes(session: Session) -> list[ReasonCode]:
    """Get all planned reason codes."""
    try:
        reason_codes = session.scalars(
            select(ReasonCode).where(ReasonCode.is_planned == True)
        )
        return list(reason_codes)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []


def get_unplanned_reason_codes(session: Session) -> list[ReasonCode]:
    """Get all unplanned reason codes."""
    try:
        reason_codes = session.scalars(
            select(ReasonCode).where(ReasonCode.is_planned == False)
        )
        return list(reason_codes)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []


def update_reason_code(
    session: Session,
    code: str,
    description: str | None = None,
    is_planned: bool | None = None,
) -> ReasonCode | None:
    """Update a reason code. Returns None if not found."""
    try:
        reason_code = session.get(ReasonCode, code)
        if reason_code is not None:
            if description is not None:
                reason_code.description = description
            if is_planned is not None:
                reason_code.is_planned = is_planned
            session.commit()
        return reason_code
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None


def delete_reason_code(session: Session, code: str, is_admin: bool = False) -> bool:
    """Delete a reason code. Returns True if deleted, False if not found or unauthorized."""
    try:
        reason_code = session.get(ReasonCode, code)
        if reason_code is not None:
            session.delete(reason_code)
            session.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return False


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
) -> ProductionRun | None:
    """Create a new production run (scheduled, not yet started)."""
    production_run = ProductionRun(
        machine_id=machine_id,
        shift_id=shift_id,
        operator_id=operator_id,
        planned_start_time=planned_start_time,
        planned_end_time=planned_end_time
    )
    try:
        session.add(production_run)
        session.commit()
        return production_run
    except IntegrityError:
        session.rollback()
        print("Error: Production Run already exists")
        return None
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None

def get_production_run(session: Session, run_id: int) -> ProductionRun | None:
    """Get a production run by ID."""
    try:
        production_run = session.get(ProductionRun, run_id)
        return production_run
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None


def get_all_production_runs(session: Session) -> list[ProductionRun]:
    """Get all production runs."""
    try:
        production_runs = session.scalars(select(ProductionRun))
        return list(production_runs)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []


def get_production_runs_by_machine(
    session: Session,
    machine_id: int,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[ProductionRun]:
    """Get production runs for a machine, optionally filtered by date range."""
    try:
        statement = select(ProductionRun).where(ProductionRun.machine_id == machine_id)

        if start_date is not None:
            statement = statement.where(
                ProductionRun.actual_start_time >= start_date
            )
        if end_date is not None:
            statement = statement.where(
                ProductionRun.actual_end_time <= end_date
            )
            
        production_runs = session.scalars(statement)
        return list(production_runs)
    
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []


def get_production_runs_by_shift(
    session: Session,
    shift_id: int,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[ProductionRun]:
    """Get production runs for a shift, optionally filtered by date range."""
    try:
        statement = select(ProductionRun).where(ProductionRun.shift_id == shift_id)

        if start_date is not None:
            statement = statement.where(
                ProductionRun.actual_start_time >= start_date
            )
        if end_date is not None:
            statement = statement.where(
                ProductionRun.actual_end_time <= end_date
            )

        production_runs = session.scalars(statement)
        return list(production_runs)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []


def get_active_production_runs(session: Session) -> list[ProductionRun]:
    """Get all currently running production runs (started but not ended)."""
    try:
        statement = select(ProductionRun).where(
            ProductionRun.actual_start_time != None,
            ProductionRun.actual_end_time == None
        )
        production_runs = session.scalars(statement)
        return list(production_runs)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []


def start_run(session: Session, run_id: int) -> ProductionRun | None:
    """Start a production run. Sets actual_start_time to now. Returns None if not found."""
    try:
        production_run = session.get(ProductionRun, run_id)
        if production_run:
            production_run.actual_start_time = func.now()
            session.commit()
        return production_run
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None


def stop_run(
    session: Session,
    run_id: int,
    good_parts_count: int,
    rejected_parts_count: int,
) -> ProductionRun | None:
    """Stop a production run. Sets actual_end_time to now and part counts. Returns None if not found."""
    try:
        production_run = session.get(ProductionRun, run_id)
        if production_run:
            production_run.actual_end_time = func.now()
            production_run.good_parts_count = good_parts_count
            production_run.rejected_parts_count = rejected_parts_count
            session.commit()
        return production_run
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None


def update_production_run(
    session: Session,
    run_id: int,
    good_parts_count: int | None = None,
    rejected_parts_count: int | None = None,
) -> ProductionRun | None:
    """Update part counts on a production run. Returns None if not found."""
    try:
        production_run = session.get(ProductionRun, run_id)
        if production_run:
            if good_parts_count is not None:
                production_run.good_parts_count = good_parts_count
            if rejected_parts_count is not None:
                production_run.rejected_parts_count = rejected_parts_count
            session.commit()
        return production_run
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None


def delete_production_run(session: Session, run_id: int, is_admin: bool = False) -> bool:
    """Delete a production run. Returns True if deleted, False if not found or unauthorized."""
    try:
        production_run = session.get(ProductionRun, run_id)
        if production_run:
            session.delete(production_run)
            session.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return False


# ============================================================
# DOWNTIME EVENTS
# ============================================================

def create_downtime_event(
    session: Session,
    production_run_id: int,
    reason_code: str,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
) -> DowntimeEvent | None:
    """Create a downtime event with explicit times."""
    downtime_event = DowntimeEvent(
        production_run_id=production_run_id,
        reason_code=reason_code,
    )

    if start_time is not None:
        downtime_event.start_time=start_time
    else:
        downtime_event.start_time=func.now()

    if end_time is not None:
        downtime_event.end_time=end_time

    try:
        session.add(downtime_event)
        session.commit()
        return downtime_event
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None


def get_downtime_event(session: Session, event_id: int) -> DowntimeEvent | None:
    """Get a downtime event by ID."""
    try:
        downtime_event = session.get(DowntimeEvent, event_id)
        return downtime_event
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None


def get_downtime_events_by_run(session: Session, run_id: int) -> list[DowntimeEvent]:
    """Get all downtime events for a production run."""
    try:
        statement = select(DowntimeEvent).where(DowntimeEvent.production_run_id == run_id)
        downtime_events = session.scalars(statement)
        return list(downtime_events)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []


def get_active_downtime_events(session: Session) -> list[DowntimeEvent]:
    """Get all currently active downtime events (started but not ended)."""
    try:
        statement = select(DowntimeEvent).where(
            DowntimeEvent.start_time != None,
            DowntimeEvent.end_time == None
        )
        downtime_events = session.scalars(statement)
        return list(downtime_events)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []      

def stop_downtime(session: Session, event_id: int) -> DowntimeEvent | None:
    """Stop a downtime event. Sets end_time to now. Returns None if not found."""
    try:
        downtime_event = session.get(DowntimeEvent, event_id)
        if downtime_event:
            downtime_event.end_time = func.now()
            session.commit()
        return downtime_event
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return None


def delete_downtime_event(session: Session, event_id: int, is_admin: bool = False) -> bool:
    """Delete a downtime event. Returns True if deleted, False if not found or unauthorized."""
    try:
        downtime_event = session.get(DowntimeEvent, event_id)
        if downtime_event:
            session.delete(downtime_event)
            session.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
        return False


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
    production_run = get_production_run(session, run_id)
    
    if production_run is None:
        return None
    
    # Need actual times to calculate run time
    if production_run.actual_start_time is None or production_run.actual_end_time is None:
        return None
    
    # Calculate times
    planned_time = (production_run.planned_end_time - production_run.planned_start_time).total_seconds()
    actual_run_time = (production_run.actual_end_time - production_run.actual_start_time).total_seconds()
    
    # Subtract downtime
    downtime_events = get_downtime_events_by_run(session, run_id)
    total_downtime = 0
    for event in downtime_events:
        if event.start_time is not None and event.end_time is not None:
            total_downtime += (event.end_time - event.start_time).total_seconds()
    
    run_time = actual_run_time - total_downtime
    
    if planned_time == 0:
        return None
    
    return run_time / planned_time


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