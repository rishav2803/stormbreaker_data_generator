from sqlmodel import JSON, Column, Enum, Field, Relationship, SQLModel
from app.models.base_uuid_model import BaseUUIDModel
from app.schemas.common_schema import ProviderType, UserRole, UserStatus
from app.models.workspace_user_link_model import WorkspaceUserLink


class UserBase(SQLModel):
    name: str = Field(max_length=64, min_length=1, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    provider: ProviderType = Field(sa_column=Column(Enum(ProviderType)))
    role: UserRole = Field(sa_column=Column(Enum(UserRole)))
    status: UserStatus = Field(sa_column=Column(Enum(UserStatus)))
    password: str | None = Field(nullable=True)


class User(BaseUUIDModel, UserBase, table=True):
    __tablename__ = "user"

    workspaces: list["Workspace"] = Relationship(
        back_populates="users",
        link_model=WorkspaceUserLink,
        sa_relationship_kwargs={"lazy": "select"},
    )
