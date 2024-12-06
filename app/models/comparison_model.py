from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlmodel import JSON, TEXT, Column, Field, Relationship, SQLModel, Index

from app.models.base_uuid_model import BaseUUIDModel
from app.models.job_model import Job


class ComparisonBase(SQLModel):
    name: str = Field(index=True)
    configuration: dict = Field(
        sa_column=Column(JSON, nullable=False, default={}))
    source_dataset_id: UUID = Field(
        foreign_key="dataset.id", ondelete="CASCADE")
    target_dataset_id: UUID = Field(
        foreign_key="dataset.id", ondelete="CASCADE")
    user_id: UUID | None = Field(foreign_key="user.id", nullable=True)


class Comparison(BaseUUIDModel, ComparisonBase, table=True):
    __tablename__ = "comparison"

    source_dataset: "Dataset" = Relationship(  # noqa: F821
        sa_relationship_kwargs={
            "lazy": "select",
            "primaryjoin": "Comparison.source_dataset_id == Dataset.id",
        },
    )
    target_dataset: "Dataset" = Relationship(  # noqa: F821
        sa_relationship_kwargs={
            "lazy": "select",
            "primaryjoin": "Comparison.target_dataset_id == Dataset.id",
        },
    )

    results: list["ComparisonResult"] = Relationship(  # noqa: F821
        back_populates="comparison",
        sa_relationship_kwargs={"lazy": "select"},
    )
    user: "User" = Relationship(
        back_populates="comparisons",
        sa_relationship_kwargs={"lazy": "joined"},
    )
    alert_group: "AlertGroup" = Relationship(
        back_populates="comparison",
        sa_relationship_kwargs={"lazy": "select"},
    )

    __table_args__ = (
        Index("ix_comparison_datasets", "source_dataset_id", "target_dataset_id"),
    )


class ComparisonResultBase(SQLModel):
    result: dict = Field(sa_column=Column(JSON, nullable=False, default={}))
    comparison_id: UUID = Field(
        foreign_key="comparison.id", ondelete="CASCADE")
    job_id: int = Field(foreign_key="job.id")


class ComparisonResult(BaseUUIDModel, ComparisonResultBase, table=True):
    __tablename__ = "comparison_result"

    job: "Job" = Relationship(
        back_populates="comparison_results",
        sa_relationship_kwargs={"lazy": "select"},
    )
    comparison: "Comparison" = Relationship(
        back_populates="results",
        sa_relationship_kwargs={"lazy": "select"},
    )

    rows: list["ComparisonResultRow"] = Relationship(
        back_populates="comparison_result",
        sa_relationship_kwargs={"lazy": "select"},
    )

    __table_args__ = (
        UniqueConstraint("comparison_id", "job_id",
                         name="unique_comparison_job"),
        Index("ix_comparison_id_foreign", "comparison_id"),
    )


class ComparisonResultRowBase(SQLModel):
    row_type: str = Field(
        nullable=False,
        default="diff_values_s",
        description=(
            "possible values will be 'diff_values_s', 'diff_values_t', 'dupl_pks_t', 'dupl_pks_s',"
            "'null_pks_t', 'null_pks_s', 'excl_pks_t', 'excl_pks_s'"
        ),
    )
    row: str = Field(sa_column=Column(TEXT))
    comparison_result_id: UUID = Field(
        foreign_key="comparison_result.id", ondelete="CASCADE"
    )


class ComparisonResultRow(BaseUUIDModel, ComparisonResultRowBase, table=True):
    __tablename__ = "comparison_result_row"

    comparison_result: "ComparisonResult" = Relationship(
        back_populates="rows",
        sa_relationship_kwargs={"lazy": "select"},
    )

    __table_args__ = (
        Index("ix_comparison_result_id_foreign", "comparison_result_id"),)
