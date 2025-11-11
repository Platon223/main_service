import requests
from django.conf import settings

def call_service(service, endpoint, payload):
    response = requests.post(f"{settings.API_GATEWAY_URL}/g/{service}/{endpoint}", json=payload)
    return response