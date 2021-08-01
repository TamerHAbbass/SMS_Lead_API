from django.db.models import query
from django.http import request
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import SMSLeadSerializer
from .models import SMS_Lead_Data
from rest_framework import permissions
from rest_framework.views import APIView

from .permissions import IsOwner


class SMSLeadListAPIView(ListCreateAPIView):
    serializer_class = SMSLeadSerializer
    queryset = SMS_Lead_Data.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


    def perform_create(self, serializer):
    
        serializer.save(owner=self.request.user)


    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)




class ReviewQueueView(APIView):
    serializer_class = SMSLeadSerializer
    queryset = SMS_Lead_Data.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return SMS_Lead_Data.objects.get(uuid=request.data)

# class SMSLeadDetailAPIView(RetrieveUpdateDestroyAPIView):
#     serializer_class = SMSLeadSerializer
#     permission_classes = (permissions.IsAuthenticated, IsOwner)
#     queryset = SMS_Lead_Data.objects.all()
#     lookup_field = "uuid"


#     def perform_create(self, serializer):
#         return serializer.save(owner=self.request.data)

    
#     def get_queryset(self):
#         print(self.request.data)
#         print('hi')
#         return self.queryset.filter(owner=self.request.user)