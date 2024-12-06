from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel, Column, JSON, UniqueConstraint

from app.models.base_uuid_model import BaseUUIDModel


class ColumnBase(SQLModel):
    column_name: str = Field(nullable=False)
    column_type: str = Field(nullable=False)
    meta: dict = Field(sa_column=Column(JSON), default={})
    dataset_id: UUID = Field(foreign_key="dataset.id", index=True, ondelete="CASCADE")


class Column(BaseUUIDModel, ColumnBase, table=True):
    __tablename__ = "dataset_column"
    dataset: "Dataset" = Relationship(
        back_populates="column",
        sa_relationship_kwargs={
            "lazy": "select",
            "primaryjoin": "Column.dataset_id == Dataset.id",
        },
    )

    validations: list["Validation"] = Relationship(
        back_populates="column",
        sa_relationship_kwargs={"lazy": "select"},
    )

    __table_args__ = (
        UniqueConstraint("dataset_id", "column_name", name="unique_column_per_dataset"),
    )
