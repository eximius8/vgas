"""Model for jobs"""

from typing import TYPE_CHECKING
import uuid

from datetime import datetime, date

from sqlmodel import Field, Relationship, SQLModel, DateTime, Enum
from sqlalchemy import func, JSON

from backend.enums import JobStatus

if TYPE_CHECKING:
    from .delivery import Delivery




class Job(SQLModel, table=True):
    __tablename__ = "jobs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    site_id: str = Field(nullable=False)
    for_date: date = Field(nullable=False, alias="date")
    status: JobStatus = Field(        
        nullable=False,
        default=JobStatus.CREATED,
        sa_type=Enum(JobStatus, native_enum=False)
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={            
            'server_default': func.now(),
        },        
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,        
        nullable=False,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': func.now(),
            'server_default': func.now(),
        },
    )
    error: str | None = Field(
        default=None,
        nullable=True
    )

    deliveries: list["Delivery"] = Relationship(
        back_populates="job", cascade_delete=True, 
    )

    stats: dict = Field(
        default_factory=dict,  # Use default_factory instead of default
        nullable=False,
        sa_type=JSON  # Add sa_type parameter
    )

    @property
    def input(self) -> dict:
        return {
            "siteId": self.site_id,
            "date": self.for_date.isoformat()
        }


class JobCreate(SQLModel):
    site_id: str = Field(alias="siteId", schema_extra={"validation_alias": "siteId"})
    for_date: date = Field(alias="date", schema_extra={"validation_alias": "date"})


class JobResponse(SQLModel):
    id: uuid.UUID = Field(alias="jobId", schema_extra={"serialization_alias": "jobId"})
    status: JobStatus


class JobStatusResponse(SQLModel):
    id: uuid.UUID = Field(alias="jobId", schema_extra={"serialization_alias": "jobId"})
    status: JobStatus
    created_at: datetime = Field(alias="createdAt", schema_extra={"serialization_alias": "createdAt"})
    updated_at: datetime = Field(alias="updatedAt", schema_extra={"serialization_alias": "updatedAt"})
    input: dict
    stats: dict
    error: str | None = None