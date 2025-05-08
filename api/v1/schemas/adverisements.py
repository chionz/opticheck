from datetime import datetime
from typing import Optional, List, Union
from pydantic import BaseModel, Field, ConfigDict
import enum


class AdvertBase(BaseModel):
    """Base schema for Adverts"""

    id: str
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    budget: float

    model_config = ConfigDict(from_attributes=True)

class AdvertCreate(BaseModel):
    """Schema to create a new Advert"""

    title: str = Field(..., example="Write Blog Post")
    description: Optional[str] = Field(None, example="Draft a blog post for the marketing team")
    status: Optional[str] = Field("Pending", example="Pending")
    priority: Optional[str] = Field("Medium", example="Medium")
    due_date: Optional[datetime] = Field(None, example="2024-12-25T23:59:59Z")


class AdvertUpdate(BaseModel):
    """Schema to update a Advert"""

    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    status: Optional[str] = Field(None, example="Completed")
    priority: Optional[str] = Field(None, example="High")
    due_date: Optional[datetime] = Field(None)

class AdvertResponse(BaseModel):
    """Schema to return Advert data"""

    id: str
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AllAdvertsResponse(BaseModel):
    """Schema for returning all Adverts"""

    message: str
    status_code: int
    status: str
    page: int
    per_page: int
    total: int
    data: Union[List[AdvertResponse], List[None]]
