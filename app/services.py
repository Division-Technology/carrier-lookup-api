from .utils import (
    ORIGINAL_CARRIER_MAPPING,
    validate_and_parse_phone_number, 
    format_to_local, 
    original_carrier,
    perform_carrier_lookup
)
from .models import CarrierResponse

async def carrier_lookup_service(phone_number: str) -> CarrierResponse:
    
    valid_number = validate_and_parse_phone_number(phone_number)
    
    if not valid_number:
        return CarrierResponse(success=False, error="Invalid phone number")

    local_number = format_to_local(valid_number)
    
    original_carrier_info = original_carrier(valid_number)
    
    carrier_info = await perform_carrier_lookup(local_number)
    
    response = CarrierResponse(
        success=True,
        phone_number=local_number,
        carrier_name=carrier_info.name,
        carrier_type=carrier_info.type,
        original_carrier=original_carrier_info
        
     )
    return response
