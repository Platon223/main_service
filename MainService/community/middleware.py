import jwt
from django.conf import settings
from django.http import JsonResponse
from jwt.exceptions import InvalidTokenError, DecodeError
from .models import UsersAllowed, Community
import requests

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        actk_header = request.headers.get("Authorization")
        if not actk_header:
            return JsonResponse({"message": "No token provided"}, status=400)
        
        actk = actk_header.split(" ")[1]
        try:
            payload = jwt.decode(actk, settings.SECRET_JWT_KEY, algorithms=["HS256"])
            request.username = payload.get("sub")
        except (InvalidTokenError, DecodeError):
            return JsonResponse({"message": "Token is invalid or expired"}, status=401)
        
        res = self.get_response(request)
        return res

class CommunityAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        json_data = request.data
        community_id = json_data.get("comm_id")
        user_username = getattr(request, "username", None)

        try:
            community = Community.objects.get(pk=community_id)
            if not community.private:
                res = self.get_response(request)
                return res
        except Community.DoesNotExist:
            return JsonResponse({"message": "community not found"}, status=404)


        if request.path_info in ["/community/create"]:
            res = self.get_response(request)
            return res

        try:
            user_allowed = UsersAllowed(pk=user_id, community_id=community_id)
        except UsersAllowed.DoesNotExist:
            return JsonResponse({"message": "user not allowed"}, status=401)
        
        res = self.get_response(request)
        return res
