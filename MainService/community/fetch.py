import requests
from django.conf import settings

def call_service(service, endpoint):
    response = requests.post(f"{settings.API_GATEWAY_URL}/g/{service}/{endpoint}")
    return response