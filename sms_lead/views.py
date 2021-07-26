from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import SMS_Lead_DataSerializer
from .models import SMS_Lead_Data
from rest_framework import permissions
# Create your views here.


class SMSLeadListAPIView(ListCreateAPIView):
    serializer_class = SMS_Lead_DataSerializer
    queryset = SMS_Lead_Data.objects.all()
    permissions = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        
        return serializer.save()

    
    def get_queryset(self):
        return self.queryset.filter()


class SMSLeadDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SMS_Lead_DataSerializer
    queryset = SMS_Lead_Data.objects.all()
    permissions = (permissions.IsAuthenticated)
    lookup_field = "uuid"

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.data)

    
    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)