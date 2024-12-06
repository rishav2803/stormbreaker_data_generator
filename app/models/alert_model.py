from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel, Column, JSON, Enum, Index

from app.models.base_uuid_model import BaseUUIDModel, BaseSerialModel
from app.schemas.common_schema import AlertStatus, Severity


class AlertGroupBase(SQLModel):
    name: str | None = Field(nullable=True)
    is_incident: bool = Field(default=False)
    status: AlertStatus = Field(
        sa_column=Column(Enum(AlertStatus), default=AlertStatus.NO_STATUS)
    )
    severity: Severity | None = Field(
        sa_column=Column(Enum(Severity), default=None, nullable=True)
    )
    validation_id: UUID | None = Field(
        default=None, foreign_key="validation.id", nullable=True, ondelete="CASCADE"
    )
    comparison_id: UUID | None = Field(
        default=None, foreign_key="comparison.id", nullable=True
    )


class AlertBase(SQLModel):
    alert_group_id: int = Field(
        foreign_key="alert_group.id", nullable=False, index=True, ondelete="CASCADE"
    )
    job_id: int = Field(foreign_key="job.id", nullable=False)
    details: dict = Field(sa_column=Column(JSON), default={})


class AlertActivityBase(SQLModel):
    alert_group_id: int = Field(
        foreign_key="alert_group.id", nullable=False, index=True, ondelete="CASCADE"
    )
    details: dict = Field(sa_column=Column(JSON), default={})


class AlertGroup(BaseSerialModel, AlertGroupBase, table=True):
    __tablename__ = "alert_group"

    alerts: list["Alert"] = Relationship(
        back_populates="alert_group",
        sa_relationship_kwargs={
            "lazy": "select",
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )
    validation: "Validation" = Relationship(
        back_populates="alert_group", sa_relationship_kwargs={"lazy": "select"}
    )
    comparison: "Comparison" = Relationship(
        back_populates="alert_group", sa_relationship_kwargs={"lazy": "select"}
    )
    activities: "AlertActivity" = Relationship(
        back_populates="alert_group",
        sa_relationship_kwargs={
            "lazy": "select",
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )

    __table_args__ = (
        Index(
            "ix_alert_group_validation_comparison_id", "validation_id", "comparison_id"
        ),
    )


class Alert(BaseUUIDModel, AlertBase, table=True):
    __tablename__ = "alert"

    job: "Job" = Relationship(
        back_populates="alerts", sa_relationship_kwargs={"lazy": "select"}
    )
    alert_group: "AlertGroup" = Relationship(
        back_populates="alerts", sa_relationship_kwargs={"lazy": "select"}
    )


class AlertActivity(BaseUUIDModel, AlertActivityBase, table=True):
    __tablename__ = "alert_activity"

    alert_group: "AlertGroup" = Relationship(
        back_populates="activities", sa_relationship_kwargs={"lazy": "select"}
    )
