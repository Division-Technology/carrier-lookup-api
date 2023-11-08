from fastapi.openapi.utils import get_openapi
from app.main import app  # Import your FastAPI instance from the main application module
import json

def generate_openapi_json():
    openapi_schema = get_openapi(
        title="Carrier Lookup API",
        version="1.0.0",
        description="This is a simple API for looking up carrier information of phone numbers",
        routes=app.routes,
    )
    with open('swagger.json', 'w') as json_file:
        json.dump(openapi_schema, json_file, indent=2)

if __name__ == "__main__":
    generate_openapi_json()
