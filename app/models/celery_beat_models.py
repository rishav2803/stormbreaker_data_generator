from datetime import datetime, timezone
from sqlalchemy import (
    LargeBinary,
    MetaData,
    Numeric,
    Table,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    Sequence,
    ForeignKey,
    CheckConstraint,
    PickleType,
    UniqueConstraint,
    func,
    Enum,
)


metadata = MetaData()


# region SQLALCHEMY CELERY BEAT TABLES
PeriodEnum = Enum("days", "hours", "minutes", "seconds", "microseconds", name="period")

SolarEventEnum = Enum(
    "dawn_astronomical",
    "dawn_nautical",
    "dawn_civil",
    "sunrise",
    "solar_noon",
    "sunset",
    "dusk_civil",
    "dusk_nautical",
    "dusk_astronomical",
    name="solarevent",
)

celery_clocked_schedule_table = Table(
    "celery_clockedschedule",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("clocked_time", DateTime(timezone=True)),
)

celery_crontab_schedule_table = Table(
    "celery_crontabschedule",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("minute", String(240), nullable=False, default="*"),
    Column("hour", String(96), nullable=False, default="*"),
    Column("day_of_week", String(64), nullable=False, default="*"),
    Column("day_of_month", String(124), nullable=False, default="*"),
    Column("month_of_year", String(64), nullable=False, default="*"),
    Column("timezone", String(64), nullable=False, default="UTC"),
)


celery_interval_schedule_table = Table(
    "celery_intervalschedule",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("every", Integer, nullable=False),
    Column("period", PeriodEnum, nullable=False),
    CheckConstraint("every >= 1", name="every_positive"),
)


celery_periodic_task_table = Table(
    "celery_periodictask",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), unique=True, nullable=False),
    Column("task", String(255), nullable=False),
    Column("args", Text, nullable=False, default="[]"),
    Column("kwargs", Text, nullable=False, default="{}"),
    Column("queue", String(255)),
    Column("exchange", String(255)),
    Column("routing_key", String(255)),
    Column("headers", Text, default="{}"),
    Column("priority", Integer),
    Column("expires", DateTime(timezone=True)),
    Column("expire_seconds", Integer),
    Column(
        "one_off",
        Boolean,
        default=False,
        nullable=False,
    ),
    Column("start_time", DateTime(timezone=True)),
    Column("enabled", Boolean, default=True, nullable=False),
    Column("last_run_at", DateTime(timezone=True)),
    Column("total_run_count", Integer, nullable=False, default=0),
    Column(
        "date_changed", DateTime(timezone=True), default=func.now(), onupdate=func.now()
    ),
    Column("description", Text, default=""),
    Column("discriminator", String(20), nullable=False),
    Column("schedule_id", Integer, nullable=False),
    CheckConstraint("priority BETWEEN 0 AND 255", name="priority_range_check"),
)

celery_periodic_task_changed_table = Table(
    "celery_periodictaskchanged",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "last_update",
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.utcnow(),
    ),
)

celery_solar_schedule_table = Table(
    "celery_solarschedule",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("event", SolarEventEnum, nullable=False),
    Column("latitude", Numeric(precision=9, scale=6, asdecimal=False), nullable=False),
    Column("longitude", Numeric(precision=9, scale=6, asdecimal=False), nullable=False),
    UniqueConstraint("event", "latitude", "longitude"),
    CheckConstraint("latitude BETWEEN -90 AND 90", name="latitude_range_check"),
    CheckConstraint("longitude BETWEEN -180 AND 180", name="longitude_range_check"),
)

# endregion

# region CELEERY TASK TABLES
celery_taskmeta_table = Table(
    "celery_taskmeta",
    metadata,
    Column(
        "id",
        Integer,
        Sequence("task_id_sequence"),
        primary_key=True,
        autoincrement=True,
    ),
    Column("task_id", String(155), unique=True, nullable=False),
    Column(
        "status", String(50), default="PENDING"
    ),  # 50 is the max length of celery states
    Column("result", PickleType, nullable=True),
    Column(
        "date_done",
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=True,
        onupdate=datetime.now(timezone.utc),
    ),
    Column("traceback", Text, nullable=True),
    Column("name", String(155), nullable=True),
    Column("args", LargeBinary, nullable=True),
    Column("kwargs", LargeBinary, nullable=True),
    Column("worker", String(155), nullable=True),
    Column("retries", Integer, nullable=True),
    Column("queue", String(155), nullable=True),
)

celery_taskset_table = Table(
    "celery_tasksetmeta",
    metadata,
    Column(
        "id",
        Integer,
        Sequence("taskset_id_sequence"),
        primary_key=True,
        autoincrement=True,
    ),
    Column("taskset_id", String(155), unique=True),
    Column("result", PickleType, nullable=True),
    Column("date_done", DateTime, default=datetime.now(timezone.utc), nullable=True),
)


celery_schedule_task_table = Table(
    "celery_schedule_taskrun",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "schedule_task_name",
        String(155),
        ForeignKey("celery_periodictask.name"),
        nullable=False,
    ),
    Column(
        "task_id", String(155), ForeignKey("celery_taskmeta.task_id"), nullable=False
    ),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
)

# endregion
