from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel, Column, JSON, Enum

from app.models.base_uuid_model import BaseSerialModel, BaseUUIDModel
from app.schemas.common_schema import SourceType


class JobBase(SQLModel):
    name: str = Field(nullable=True)
    """
    Use this information to create random values
    {
        "status": "pending|running|completed|failed",
    }
    """
    meta: dict = Field(sa_column=Column(JSON))
    comparison_id: UUID | None = Field(
        foreign_key="comparison.id", nullable=True, ondelete="SET NULL"
    )
    validation_id: UUID | None = Field(
        foreign_key="validation.id", nullable=True, ondelete="SET NULL"
    )
    is_interactive: bool = Field(default=False, nullable=False)
    origin: SourceType = Field(sa_column=Column(Enum(SourceType)))


class Job(BaseSerialModel, JobBase, table=True):
    __tablename__ = "job"

    comparison_results: "ComparisonResult" = Relationship(  # noqa: F821
        back_populates="job",
        sa_relationship_kwargs={"lazy": "select", "uselist": False},
    )
    validation_results: "ValidationResult" = Relationship(  # noqa: F821
        back_populates="job",
        sa_relationship_kwargs={"lazy": "select"},
    )
    alerts: "Alert" = Relationship(  # noqa: F821
        back_populates="job",
        sa_relationship_kwargs={"lazy": "select"},
    )
