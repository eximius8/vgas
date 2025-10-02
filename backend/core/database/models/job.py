"""Model for jobs"""

from typing import TYPE_CHECKING
import uuid

from datetime import datetime, date

from sqlmodel import Field, Relationship, SQLModel, DateTime, Enum
from sqlalchemy import func, JSON

from backend.enums import JobStatusEnum

if TYPE_CHECKING:
    from .delivery import Delivery


class Job(SQLModel, table=True):
    __tablename__ = "jobs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    site_id: str = Field(nullable=False)
    for_date: date = Field(nullable=False, alias="date")
    status: JobStatusEnum = Field(
        nullable=False,
        default=JobStatusEnum.CREATED,
        sa_type=Enum(JobStatusEnum, native_enum=False),
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": func.now(),
            "server_default": func.now(),
        },
    )
    error: str | None = Field(default=None, nullable=True)

    deliveries: list["Delivery"] = Relationship(
        back_populates="job",
        cascade_delete=True,
    )

    stats: dict = Field(
        default_factory=dict,  # Use default_factory instead of default
        nullable=False,
        sa_type=JSON,  # Add sa_type parameter
    )

    @property
    def input(self) -> dict:
        return {"siteId": self.site_id, "date": self.for_date.isoformat()}
