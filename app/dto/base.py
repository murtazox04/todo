import datetime

from pydantic import BaseModel, Field


def serialize_time(value: datetime.datetime) -> str:
    return value.strftime("%H:%M %d.%m.%Y")


class Base(BaseModel):

    id: int
    created_at: datetime.datetime = Field(alias='createdAt')
    updated_at: datetime.datetime = Field(alias='updatedAt')

    class Config:
        json_encoders = {
            datetime.datetime: serialize_time
        }
        orm_mode = True
        allow_population_by_field_name = True
