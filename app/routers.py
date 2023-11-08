from fastapi import APIRouter, HTTPException
from .models import PhoneNumber, CarrierResponse
from .services import carrier_lookup_service

phone_router = APIRouter()

@phone_router.post("/api/v1/phone/carrier-lookup", response_model=CarrierResponse)
async def phone_carrier_lookup(phone: PhoneNumber):
    response = await carrier_lookup_service(phone.phone_number)
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Carrier information not found.")
