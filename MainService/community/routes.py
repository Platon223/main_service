from django.shortcuts import render, get_list_or_404
from .models import Community, UsersAllowed
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponseBadRequest
from .serializer import CommunitySerializer, UsersAllowedSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from django.conf import settings
from .fetch import call_service

# Create your views here.

@api_view(["GET"])
def find_community(request):
    try:
        unicode = request.body.decode('utf-8')
        data = json.loads(unicode)

        community_id = data.get('comm_id')

        if not community_id:
            return HttpResponseBadRequest("No community id provided")
        
        community = Community.objects.get(pk=community_id)

        serializer = CommunitySerializer(community)

        return JsonResponse(serializer.data)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        return HttpResponseBadRequest(f"Error occured: {e}")

@api_view(["POST"])
def create_community(request):
    user_username = getattr(request, "username", None)

    res = call_service("auth", "find_by_username", {"username": user_username})
    if res.status_code != 200:
        return JsonResponse({"message": "something went wrong"}, status=res.status_code)
    
    serializer = CommunitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(creator=res.json().get("user_id"))

        if request.data.get("private"):
            try:
                current_community = Community.objects.get(creator_id=res.json().get("user_id"))
            except Community.DoesNotExist:
                return JsonResponse({"message": "community not found"}, status=404)
            users_allowed_serializer = UsersAllowedSerializer(data={"user_id": res.json().get("user_id"), "community_id": current_community.id})
            if users_allowed_serializer.is_valid():
                users_allowed_serializer.save()
            else:
                return JsonResponse({"message": f"error occured: {users_allowed_serializer.errors}"}, status=400)
            
        return JsonResponse({"message": "success"}, status=200)
    return JsonResponse({"message": f"error occured: {serializer.errors}"}, status=400)

@api_view(["POST"])
def join_community(request):
    json_data = request.data
    comm_id = json_data.get("comm_id")
    user_username = getattr(request, "username", None)

    try:
        community = Community.objects.get(pk=comm_id)
        community_creator_id = community.creator_id
    except Community.DoesNotExist:
        return JsonResponse({"message": "Community not found"})

    # Send a message to the queue for the auth service

    return JsonResponse({"message": f"notification sent to: {community_creator_id}, {user_username} is waiting for response"})

@api_view(["POST"])
def allow_users_join(request):
    json_data = request.data
    community_id = json_data.get("comm_id")
    allowed_user_id = json_data.get("allowed_user")
    user_id = getattr(request, "id", None)

    try:
        community = Community.objects.get(pk=community_id, creator_id=user_id)

        if UsersAllowed.objects.filter(user_id=allowed_user_id).exists():
            return JsonResponse({"message": "user is already allowed"}, status=400)

        UsersAllowed.objects.create(user_id=allowed_user_id, community_id=community_id)
    except Community.DoesNotExist:
        return JsonResponse({"message": "user is not a creator"}, status=401)
    
    return JsonResponse({"message": "user allowed successufully"}, status=200)

@api_view(["DELETE"])
def delete_allowed_user(request):
    json_data = request.data
    deleted_user = json_data.get("delete_user")
    creator_id = getattr(request, "id", None)
    community_id = json_data.get("comm_id")

    try:
        pass
    except:
        pass
    

    












    


