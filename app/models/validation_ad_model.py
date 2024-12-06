from uuid import UUID
from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlmodel import JSON, Column as SqlColumn, Field, Relationship, SQLModel, Index

from app.models.base_uuid_model import BaseUUIDModel


class ValidationADPredictionBase(SQLModel):
    validation_id: UUID = Field(
        foreign_key="validation.id", nullable=False, ondelete="CASCADE"
    )
    date: datetime = Field(nullable=False)
    hour: int = Field(nullable=False, default=0, ge=0, le=23)
    details: dict = Field(sa_column=SqlColumn(JSON), default={})


class ValidationADPrediction(BaseUUIDModel, ValidationADPredictionBase, table=True):
    __tablename__ = "validation_ad_prediction"

    validation: "Validation" = Relationship(
        back_populates="thresholds",
        sa_relationship_kwargs={"lazy": "joined"},
    )

    __table_args__ = (
        UniqueConstraint(
            "validation_id", "date", "hour", name="unique_validation_threshold"
        ),
        Index("ix_validation_threshold", "validation_id", "date", "hour"),
    )


class ValidationADModelBase(SQLModel):
    validation_id: UUID = Field(
        foreign_key="validation.id", nullable=False, index=True, ondelete="CASCADE"
    )
    model: dict = Field(sa_column=SqlColumn(JSON))


class ValidationADModel(BaseUUIDModel, ValidationADModelBase, table=True):
    __tablename__ = "validation_ad_model"

    validation: "Validation" = Relationship(
        back_populates="models",
        sa_relationship_kwargs={"lazy": "joined"},
    )
