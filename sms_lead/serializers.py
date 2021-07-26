from rest_framework import serializers
from .models import SMS_Lead_Data


class SMS_Lead_DataSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = SMS_Lead_Data

        fields = "__all__"