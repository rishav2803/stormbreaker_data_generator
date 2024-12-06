
import enum
from uuid import UUID

from sqlmodel import JSON, Column, Enum, Field, Relationship, SQLModel, Index
from sqlalchemy import UniqueConstraint

from app.models import *
from app.models.base_uuid_model import BaseUUIDModel
from app.schemas.common_schema import DataSourceType, SourceType


class DataSourceBase(SQLModel):
    name: str = Field(index=True, max_length=255, min_length=1, nullable=False)
    type: DataSourceType = Field(sa_column=Column(Enum(DataSourceType)))
    connection: dict = Field(sa_column=Column(JSON))
    is_interactive: bool = Field(default=False, nullable=False)
    origin: SourceType = Field(sa_column=Column(Enum(SourceType)))
    workspace_id: UUID = Field(foreign_key="workspace.id")
    schedule: str = Field(
        max_length=64, min_length=1, nullable=False, default="0 0 * * *"
    )
    user_id: UUID | None = Field(foreign_key="user.id", nullable=True)


class DataSource(BaseUUIDModel, DataSourceBase, table=True):
    __tablename__ = "datasource"
    workspace: "Workspace" = Relationship(  # noqa: F821
        back_populates="data_sources", sa_relationship_kwargs={"lazy": "select"}
    )
    datasets: list["Dataset"] | None = Relationship(  # noqa: F821
        back_populates="data_source",
        sa_relationship_kwargs={"lazy": "select"},
    )
    user: "User" = Relationship(
        back_populates="data_sources",
        sa_relationship_kwargs={"lazy": "select"},
    )
    __table_args__ = (
        UniqueConstraint("name"),
        Index("ix_workspace_id_foreign", "workspace_id"),
    )
