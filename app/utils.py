# Include your functions like validate_and_parse_phone_number, format_to_local, 
# original_carrier, perform_carrier_lookup, etc.

import re
from typing import Optional

# Declare constants
COUNTRY_CODE = '+374'
CARRIER_PREFIXES = [
    "55", "95", "41", "60", "44", "91", "99", "96", "33", "43", "10", "98", "93", "77", "94", "97"
]
NUMBER_LENGTH = 6
CARRIERS = ["Ucom GSM (Ucom)", "Team Telecom", "MTS Armenia GSM (Vivacell MTS)", "KT Telecom"]

# Define the original carrier mapping
ORIGINAL_CARRIER_MAPPING = {
    "55": "Ucom GSM (Ucom)",
    "95": "Ucom GSM (Ucom)",
    "33": "Ucom GSM (Ucom)",
    "41": "Ucom GSM (Ucom)",
    "44": "Ucom GSM (Ucom)",
    "91": "Team Telecom",
    "99": "Team Telecom",
    "96": "Team Telecom",
    "43": "Team Telecom",
    "97": "KT Telecom",
    "98": "MTS Armenia GSM (Vivacell MTS)",
    "93": "MTS Armenia GSM (Vivacell MTS)",
    "77": "MTS Armenia GSM (Vivacell MTS)",
    "94": "MTS Armenia GSM (Vivacell MTS)"
}

def validate_and_parse_phone_number(phone_number: str) -> Optional[str]:
    # Remove any spaces or hyphens that might be present
    phone_number = re.sub(r"[ -]", "", phone_number)
    
    # Regular expression to validate the phone number
    pattern = re.compile(r"^(00374|\+374|374|0)?(" + '|'.join(CARRIER_PREFIXES) + r")\d{" + str(NUMBER_LENGTH) + r"}$")
    
    match = pattern.fullmatch(phone_number)
    if match:
        prefix, number = match.groups()[1], phone_number[-NUMBER_LENGTH:]
        return f"{COUNTRY_CODE}{prefix}{number}"
    else:
        return None

def format_to_local(phone_number: str) -> Optional[str]:
    # Validate and parse the number first
    international_number = validate_and_parse_phone_number(phone_number)
    if international_number:
        return f"0{international_number[-(NUMBER_LENGTH + 2):]}"
    else:
        return None

def original_carrier(phone_number: str) -> Optional[str]:
    # Validate and parse the number first
    international_number = validate_and_parse_phone_number(phone_number)
    if international_number:
        carrier_prefix = international_number[4:6]  # Extracting carrier prefix
        return ORIGINAL_CARRIER_MAPPING.get(carrier_prefix, "Unknown")
    else:
        return None
    
import requests

def post_request(url, endpoint, payload):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url + endpoint, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed with status code {response.status_code}")

def perform_carrier_lookup(original_carrier, phone_number):
    carriers = {
        "MTS Armenia GSM (Vivacell MTS)": {
            "base_url": "https://cabinet.mts.am/Epay2/api/epayapi",
            "endpoint": "/GetDebt",
            "payload": {"Phone": phone_number},
            "fallback_url": "https://itfllc.am/api/payments/guest/utility/findResult",
            "fallback_endpoint": "/viva-cell-mobile-itf",
            "fallback_payload": {"lang": "en", "phone": phone_number}
        },
        "Team Telecom": {
            "base_url": "https://itfllc.am/api/payments/guest/utility/findResult",
            "endpoint": "/beeline-mobile",
            "payload": {"lang": "en", "phone": phone_number}
        },
        "Ucom GSM (Ucom)": {
            "base_url": "https://itfllc.am/api/payments/guest/utility/findResult",
            "endpoint": "/ucom_mobile",
            "payload": {"lang": "en", "phone": phone_number},
            "fallback_endpoint": "/ucom-mobile-business"
        }
    }
    
    sequence = {
        "MTS Armenia GSM (Vivacell MTS)": ["Team Telecom", "Ucom GSM (Ucom)"],
        "Team Telecom": ["Ucom GSM (Ucom)", "MTS Armenia GSM (Vivacell MTS)"],
        "Ucom GSM (Ucom)": ["MTS Armenia GSM (Vivacell MTS)", "Team Telecom"]
    }
    
    try:
        # Try the original carrier first
        carrier_info = carriers[original_carrier]
        response = post_request(carrier_info["base_url"], carrier_info["endpoint"], carrier_info["payload"])
        if response.get("status", False) or response.get("IsNumberExist", False):
            return response
        
        # If original carrier request fails and it has a fallback, try that
        if 'fallback_url' in carrier_info:
            response = post_request(carrier_info["fallback_url"], carrier_info["fallback_endpoint"], carrier_info["fallback_payload"])
            if response.get("status", False):
                return response
        
        # If it fails or has no fallback, try the next carrier in sequence
        for next_carrier in sequence[original_carrier]:
            next_carrier_info = carriers[next_carrier]
            response = post_request(next_carrier_info["base_url"], next_carrier_info["endpoint"], next_carrier_info["payload"])
            if response.get("status", False):
                return response
            
            # Special fallback for Ucom in case of failure
            if next_carrier == "Ucom GSM (Ucom)" and not response.get("status", False):
                response = post_request(next_carrier_info["base_url"], next_carrier_info["fallback_endpoint"], next_carrier_info["payload"])
                if response.get("status", False):
                    return response
            
        # If all attempts fail
        return {"message": "All carrier checks failed or user not found", "status": False}
        
    except Exception as e:
        return {"message": str(e), "status": False}
