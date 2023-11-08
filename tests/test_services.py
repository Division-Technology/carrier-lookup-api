import pytest
from app.services import carrier_lookup_service

# Mock data for testing
test_data = [
    ("0770123456", True),
    ("07701234", False)  # Invalid format
]

@pytest.mark.parametrize("phone_number, expected", test_data)
def test_carrier_lookup_service(phone_number, expected):
    result = carrier_lookup_service(phone_number)
    if expected:
        assert result is not None
        assert result.original_carrier is not None  # or any other key field
    else:
        assert result is None
