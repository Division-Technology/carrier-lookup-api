import pytest
from app.utils import validate_and_parse_phone_number, format_to_local, original_carrier

# More test cases can be added accordingly
@pytest.mark.parametrize("phone_number, expected", [
    ("+37455987654", "+37455987654"),
    ("0037455987654", "+37455987654"),
    ("055987654", "+37455987654"),
    ("incorrect_number", None)
])
def test_validate_and_parse_phone_number(phone_number, expected):
    assert validate_and_parse_phone_number(phone_number) == expected

@pytest.mark.parametrize("phone_number, expected", [
    ("+37455987654", "055987654"),
    ("incorrect_number", None)
])
def test_format_to_local(phone_number, expected):
    assert format_to_local(phone_number) == expected

@pytest.mark.parametrize("phone_number, expected", [
    ("+37455987654", "Ucom GSM (Ucom)"),
    ("+37491987654", "Team Telecom"),
    ("incorrect_number", None)
])
def test_original_carrier(phone_number, expected):
    assert original_carrier(phone_number) == expected
