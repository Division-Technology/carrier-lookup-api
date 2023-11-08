from pydantic import BaseModel, Field

class PhoneNumber(BaseModel):
    phone_number: str = Field(..., example="0770123456")

class CarrierResponse(BaseModel):
    initial_number: str
    local_format: str
    international_format: str
    original_carrier: str
    current_carrier: str
