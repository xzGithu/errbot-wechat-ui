from rest_framework import serializers
from useraction.models import commands

class CommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model=commands
        fields='__all__'