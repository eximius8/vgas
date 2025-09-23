"""Model for jobs"""

from typing import TYPE_CHECKING
import uuid
import enum
from datetime import datetime, date

from sqlmodel import Field, Relationship, SQLModel, DateTime, Enum

if TYPE_CHECKING:
    from .delivery import Delivery


class JobStatus(str, enum.Enum):
    CREATED = "created"
    PROCESSING = "processing"
    FINISHED = "finished"
    FAILED = "failed"


class Job(SQLModel, table=True):   

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    site_id: str = Field(nullable=False)
    for_date: date = Field(nullable=False, alias="date")
    status: JobStatus = Field(
        Enum(JobStatus, name="job_status", native_enum=False),
        nullable=False,
        default=JobStatus.CREATED,
    )
    created_at: datetime = Field(
        DateTime(timezone=True), default=datetime.now(), nullable=False
    )
    updated_at: datetime = Field(
        DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now(), nullable=False
    )    
    error: str | None = Field(
        nullable=True
    )

    deliveries: list["Delivery"] = Relationship(
        back_populates="job", cascade_delete=True, 
    )


class JobCreate(SQLModel):
    site_id: str = Field(alias="siteId")
    for_date: date = Field(alias="date")


class JobResponse(SQLModel):
    id: uuid.UUID = Field(alias="jobId")
    status: JobStatus
