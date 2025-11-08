from django.urls import path
from . import routes

urlpatterns = [
    path('find', routes.find_community),
    path('create', routes.create_community),
    path('join', routes.join_community)
]