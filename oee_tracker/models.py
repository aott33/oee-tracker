from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Machine(Base):
    __tablename__ = "machines"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    ideal_cycle_time: Mapped[float] = mapped_column(Float, nullable=False)
    location: Mapped[str | None] = mapped_column(String)

    production_runs: Mapped[list["ProductionRun"]] = relationship(back_populates="machine")


class Shift(Base):
    __tablename__ = "shifts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    production_runs: Mapped[list["ProductionRun"]] = relationship(back_populates="shift")


class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    production_runs: Mapped[list["ProductionRun"]] = relationship(back_populates="operator")


class ReasonCode(Base):
    __tablename__ = "reason_codes"

    code: Mapped[str] = mapped_column(String, primary_key=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    is_planned: Mapped[bool] = mapped_column(Boolean, default=False)

    downtime_events: Mapped[list["DowntimeEvent"]] = relationship(back_populates="reason")


class ProductionRun(Base):
    __tablename__ = "production_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id", ondelete="CASCADE"))
    shift_id: Mapped[int] = mapped_column(ForeignKey("shifts.id", ondelete="CASCADE"))
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id", ondelete="CASCADE"))
    planned_start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    planned_end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    actual_start_time: Mapped[datetime | None] = mapped_column(DateTime)
    actual_end_time: Mapped[datetime | None] = mapped_column(DateTime)
    good_parts_count: Mapped[int | None] = mapped_column(Integer)
    rejected_parts_count: Mapped[int | None] = mapped_column(Integer)

    machine: Mapped["Machine"] = relationship(back_populates="production_runs")
    shift: Mapped["Shift"] = relationship(back_populates="production_runs")
    operator: Mapped["Operator"] = relationship(back_populates="production_runs")
    downtime_events: Mapped[list["DowntimeEvent"]] = relationship(back_populates="production_run")


class DowntimeEvent(Base):
    __tablename__ = "downtime_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    production_run_id: Mapped[int] = mapped_column(ForeignKey("production_runs.id", ondelete="CASCADE"))
    reason_code: Mapped[str] = mapped_column(ForeignKey("reason_codes.code", ondelete="CASCADE"))
    start_time: Mapped[datetime | None] = mapped_column(DateTime)
    end_time: Mapped[datetime | None] = mapped_column(DateTime)

    production_run: Mapped["ProductionRun"] = relationship(back_populates="downtime_events")
    reason: Mapped["ReasonCode"] = relationship(back_populates="downtime_events")