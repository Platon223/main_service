from django.shortcuts import render, get_list_or_404
from .models import Community
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponseBadRequest

# Create your views here.

@csrf_exempt
def find_community(request):
    try:
        unicode = request.body.decode('utf-8')
        data = json.loads(unicode)

        community_id = data.get('comm_id')

        if not community_id:
            return HttpResponseBadRequest("No community id provided")
        
        community = Community.objects.get(pk=community_id)

        return JsonResponse({"message": f"community found: {community.name}"})
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        return HttpResponseBadRequest(f"Error occured: {e}")



