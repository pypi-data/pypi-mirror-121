from rest_framework import serializers


class InfoSerializer(serializers.Serializer):
    app = serializers.CharField()
    version = serializers.CharField()
