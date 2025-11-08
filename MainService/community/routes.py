from django.shortcuts import render, get_list_or_404
from .models import Community
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponseBadRequest
from .serializer import CommunitySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from django.conf import settings

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

    response = requests.get(f"{settings.API_GATEWAY_URL}/find_by_username")
    if response.status_code == 200:
        user_id_json = response.json()
    else:
        return JsonResponse({"message": "something went wrong"}, status=response.status_code)
    
    serializer = CommunitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(creator=user_id_json.get("user_id"))
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







    


