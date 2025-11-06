from rest_framework import serializers


class CommunitySerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    private = serializers.BooleanField()
    members = serializers.IntegerField()
    publish_date = serializers.DateField()

