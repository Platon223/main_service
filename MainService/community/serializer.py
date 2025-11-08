from rest_framework import serializers
from .models import Community


class CommunitySerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    private = serializers.BooleanField()
    members = serializers.IntegerField()
    publish_date = serializers.DateField()
    creator_id = serializers.CharField()

    def create(self, data):
        data["id"] = 'generate_id'
        creator = data.pop("creator")
        data["creator_id"] = creator

        return Community.objects.create(**data)

