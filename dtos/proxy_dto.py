from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class ProxyAvailabilityDTO(BaseModel):
    telegram_id: int
    version: str = Field(..., min_length=1)
    country: str = Field(..., min_length=2, max_length=3)
    quantity: int = Field(..., gt=0)


class ProxyAvailabilityResponse(BaseModel):
    success: bool
    available: bool
    available_quantity: int


class ProxyGetPriceDTO(BaseModel):
    telegram_id: int
    version: str = Field(..., min_length=1)
    days: int = Field(..., ge=1, le=180)
    quantity: int = Field(..., gt=0)

    @field_validator('days')
    def must_be_integer(cls, v):
        if not isinstance(v, int):
            raise ValueError("Period must be an integer")
        return v


class ProxyGetPriceResponse(BaseModel):
    success: bool
    available: bool
    total_price: float


class ProxyProcessBuyingDTO(BaseModel):
    telegram_id: str
    version: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)
    country: str = Field(..., min_length=2, max_length=3)
    days: int = Field(..., ge=1, le=180)
    quantity: int = Field(..., gt=0)
    auto_prolong: bool


class ProxyItem(BaseModel):
    ip: str
    host: str
    port: int
    type: str
    version: str
    country: str
    date: datetime
    date_end: datetime
    unixtime: int
    unixtime_end: int
    descr: Optional[str] = None
    active: bool
    auto_prolong: bool | None = None


class ProxyProcessBuyingResponse(BaseModel):
    success: bool
    status_code: int
    error: str
    list: List[ProxyItem]
    quantity: int
    price: float
    days: int
    country: str


class ProxyUsersListResponse(BaseModel):
    success: bool
    status_code: int
    error: str
    list: List[ProxyItem]