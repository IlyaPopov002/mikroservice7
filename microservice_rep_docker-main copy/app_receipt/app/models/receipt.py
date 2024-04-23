import enum
from uuid import UUID
from datetime import datetime
from pydantic import ConfigDict, BaseModel
from typing import Optional


class Receipt(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rec_id: UUID
    ord_id: UUID
    type: str
    customer_info: str
    create_date: datetime
    rec: str


class CreateReceiptRequest(BaseModel):
    ord_id: UUID
    type: str
    rec: str
    customer_info: str
