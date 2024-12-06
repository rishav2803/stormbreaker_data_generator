from uuid import UUID

from sqlmodel import (
    JSON,
    Column as SqlColumn,
    Field,
    Relationship,
    SQLModel,
    Enum,
    Index,
)

from app.models.base_uuid_model import BaseUUIDModel
from app.models.job_model import Job
from app.models.user_model import User
from app.schemas.common_schema import AutoStatus, ValidationCategory


class ValidationBase(SQLModel):
    name: str = Field(index=True, max_length=64, min_length=1, nullable=False)
    configuration: dict = Field(sa_column=SqlColumn(JSON))
    type: str | None = Field(max_length=64, nullable=True)
    is_auto: bool = Field(default=False)
    is_paused: bool = Field(default=False, nullable=False)
    auto_status: str | None = Field(
        sa_column=SqlColumn(Enum(AutoStatus), nullable=True)
    )
    category: str = Field(sa_column=SqlColumn(Enum(ValidationCategory), nullable=False))
    dataset_id: UUID | None = Field(
        foreign_key="dataset.id", nullable=True, ondelete="CASCADE"
    )
    column_id: UUID | None = Field(
        foreign_key="dataset_column.id", nullable=True, ondelete="SET NULL"
    )
    user_id: UUID | None = Field(foreign_key="user.id", nullable=True)
    schedule: str = Field(
        max_length=64, min_length=1, nullable=False, default="0 0 * * *"
    )


class Validation(BaseUUIDModel, ValidationBase, table=True):
    __tablename__ = "validation"

    dataset: "Dataset" = Relationship(  # noqa: F821
        back_populates="validations",
        sa_relationship_kwargs={"lazy": "select"},
    )
    validation_results: list["ValidationResult"] = Relationship(
        back_populates="validation",
        sa_relationship_kwargs={
            "lazy": "select",
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )
    column: "Column" = Relationship(
        back_populates="validations",
        sa_relationship_kwargs={"lazy": "select"},
    )
    user: "User" = Relationship(
        back_populates="validations",
        sa_relationship_kwargs={"lazy": "select"},
    )
    thresholds: list["ValidationADPrediction"] = Relationship(
        back_populates="validation",
        sa_relationship_kwargs={
            "lazy": "select",
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )
    models: list["ValidationADModel"] = Relationship(
        back_populates="validation",
        sa_relationship_kwargs={
            "lazy": "select",
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )
    alert_group: "AlertGroup" = Relationship(
        back_populates="validation",
        sa_relationship_kwargs={
            "lazy": "select",
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )

    __table_args__ = (Index("ix_dataset_column", "dataset_id", "column_id"),)


class ValidationResultBase(SQLModel):
    value: int = Field(nullable=False)
    status: str | None = Field(max_length=64, nullable=True)
    reason: str | None = Field(max_length=255, nullable=True)
    validation_id: UUID = Field(foreign_key="validation.id", ondelete="CASCADE")
    job_id: int | None = Field(foreign_key="job.id", nullable=True)


class ValidationResult(BaseUUIDModel, ValidationResultBase, table=True):
    __tablename__ = "validation_result"

    validation: "Validation" = Relationship(
        back_populates="validation_results", sa_relationship_kwargs={"lazy": "select"}
    )
    job: "Job" = Relationship(
        back_populates="validation_results",
        sa_relationship_kwargs={"lazy": "select"},
    )
