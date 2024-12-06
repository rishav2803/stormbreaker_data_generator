from uuid import UUID

from sqlmodel import (
    Field,
    JSON,
    Relationship,
    Column as SqlColumn,
    SQLModel,
    UniqueConstraint,
    Index,
)

from app.models.base_uuid_model import BaseUUIDModel
from app.models.comparison_model import Comparison
from app.models.data_source_model import DataSource
from app.models.validation_model import Validation
from app.models.column_model import Column


class DatasetBase(SQLModel):
    name: str = Field(max_length=255, min_length=1, nullable=False)
    meta_data: dict = Field(sa_column=SqlColumn(JSON, nullable=False, default={}))
    data_source_id: UUID = Field(foreign_key="datasource.id", ondelete="CASCADE")


class Dataset(BaseUUIDModel, DatasetBase, table=True):
    __tablename__ = "dataset"

    data_source: "DataSource" = Relationship(
        back_populates="datasets",
        sa_relationship_kwargs={"lazy": "select"},
    )

    validations: list["Validation"] = Relationship(
        back_populates="dataset",
        sa_relationship_kwargs={"lazy": "select"},
    )

    column: list["Column"] = Relationship(back_populates="dataset")

    __table_args__ = (
        UniqueConstraint("name", "data_source_id", name="unique_dataset_name"),
        Index("ix_dsname_dsid", "name", "data_source_id"),
    )
