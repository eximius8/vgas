
"""Model for jobs"""


import uuid

from datetime import datetime, date

from datetime import datetime
from pydantic import BaseModel, Field



from backend.enums import JobStatusEnum



class JobCreateSerializer(BaseModel):
    site_id: str = Field(alias="siteId", schema_extra={"validation_alias": "siteId"})
    for_date: date = Field(alias="date", schema_extra={"validation_alias": "date"})


class JobGetSerializer(BaseModel):
    id: uuid.UUID = Field(alias="jobId", schema_extra={"serialization_alias": "jobId"})
    status: JobStatusEnum


class JobStatusSerializer(BaseModel):
    id: uuid.UUID = Field(alias="jobId", schema_extra={"serialization_alias": "jobId"})
    status: JobStatusEnum
    created_at: datetime = Field(alias="createdAt", schema_extra={"serialization_alias": "createdAt"})
    updated_at: datetime = Field(alias="updatedAt", schema_extra={"serialization_alias": "updatedAt"})
    input: dict
    stats: dict
    error: str | None = None