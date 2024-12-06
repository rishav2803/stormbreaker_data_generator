from sqlmodel import JSON, Column, Enum, Field, Relationship, SQLModel
from app.models.base_uuid_model import BaseUUIDModel

from uuid import UUID
from datetime import datetime
from app.schemas.common_schema import InvitationStatus


class InvitationBase(SQLModel):
    inviter_user_id: UUID = Field(foreign_key="user.id", nullable=False)
    invitee_name: str = Field(nullable=False)
    invitee_email: str = Field(index=True, unique=True, nullable=False)
    token: str = Field(unique=True, nullable=False)
    details: dict = Field(sa_column=Column(JSON), default={})
    status: InvitationStatus = Field(sa_column=Column(Enum(InvitationStatus)))
    expires_at: datetime = Field(nullable=False)


class Invitation(BaseUUIDModel, InvitationBase, table=True):
    __tablename__ = "user_invitation"

    user: "User" = Relationship(back_populates="invites")
