"""Model for jobs"""

import uuid

from datetime import datetime, date

from pydantic import BaseModel, Field


from backend.enums import JobStatusEnum


class JobCreateSerializer(BaseModel):
    site_id: str = Field(alias="siteId", validation_alias="siteId")
    for_date: date = Field(alias="date", validation_alias="date")


class JobGetSerializer(BaseModel):
    id: uuid.UUID = Field(serialization_alias="jobId")
    status: JobStatusEnum


class JobStatusSerializer(BaseModel):
    id: uuid.UUID = Field(serialization_alias="jobId")
    status: JobStatusEnum
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")
    input: dict
    stats: dict
    error: str | None = None
