from rest_framework import serializers
from . import models


class UrlKeyHashSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('key', 'url', 'user', 'created_at', 'updated_at',)
        model = models.User
