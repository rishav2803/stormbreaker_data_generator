from uuid import UUID
from sqlmodel import JSON, Column, Enum, Field, Relationship, SQLModel

from app.schemas.common_schema import UserActivityType
from app.models.base_uuid_model import BaseUUIDModel


class ActivityBase(SQLModel):
    user_id: UUID = Field(foreign_key="user.id", nullable=False, index=True)
    activity_type: UserActivityType = Field(sa_column=Column(Enum(UserActivityType)))
    details: dict = Field(sa_column=Column(JSON), default={})


class Activity(BaseUUIDModel, ActivityBase, table=True):
    __tablename__ = "user_activity"

    user: "User" = Relationship(
        back_populates="activities",
        sa_relationship_kwargs={"lazy": "joined"},
    )
