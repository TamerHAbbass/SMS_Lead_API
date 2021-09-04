from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponse
from django.views import generic
from django.views.generic import ListView
from rest_framework.generics import ListAPIView

from sms_lead.models import Sent_Call_List, SMS_Successful
import datetime


class DailySMSSuccessSummaryView(generic.View):

    def get(self, request):
        queryset = SMS_Successful.objects.all().order_by('updated')
        query_list = []
        for query in queryset:
            if (datetime.datetime.now() - datetime.timedelta(hours=24)) < query.updated.replace(tzinfo=None) and datetime.datetime.now() > query.updated.replace(tzinfo=None):
                query_list.append(query)
                
        return HttpResponse(str(query_list), content_type='application/json')
