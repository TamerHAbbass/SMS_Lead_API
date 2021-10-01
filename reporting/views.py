from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.views import generic
import json
from sms_lead.models import Sent_Call_List, SMS_Successful
from . import forms
import datetime
from .generate_report import generate


class DailySMSSuccessSummaryView(generic.View):

    def get(self, request):
        queryset = SMS_Successful.objects.all().order_by('updated')
        query_list = []
        for query in queryset:
            if (datetime.datetime.now() - datetime.timedelta(hours=24)) < query.updated.replace(tzinfo=None) and datetime.datetime.now() > query.updated.replace(tzinfo=None):
                query_list.append(query)

        return render(request, 'reporting/reporting.html')


class WeeklySMSSuccessSummaryView(generic.View):

    def get(self, request):
        queryset = SMS_Successful.objects.all().order_by('updated')
        query_list = []
        for query in queryset:
            if (datetime.datetime.now() - datetime.timedelta(weeks=1)) < query.updated.replace(tzinfo=None) and datetime.datetime.now() > query.updated.replace(tzinfo=None):
                query_list.append(query)

        return HttpResponse(str(len(query_list)), content_type='application/json')


class MonthlySMSSuccessSummaryView(generic.View):

    def get(self, request):
        queryset = SMS_Successful.objects.all().order_by('updated')
        query_list = []
        for query in queryset:
            if (datetime.datetime.now() - datetime.timedelta(weeks=4)) < query.updated.replace(tzinfo=None) and datetime.datetime.now() > query.updated.replace(tzinfo=None):
                query_list.append(query)

        return HttpResponse(str(len(query_list)), content_type='application/json')


class CustomSMSSuccessSummaryView(generic.View):


    def get(self, request):    
        form = forms.CustomReportRange()
        context = {'form':form}    
        return render(request, 'reporting/reportingCustomRange.html', context)


    def post(self, request):
        form = forms.CustomReportRange()
        context = {'form':form}
        startDateTime = datetime.datetime.fromisoformat(request.POST.get('startDateTime'))
        endDateTime = datetime.datetime.fromisoformat(request.POST.get('endDateTime'))
        
        queryset = SMS_Successful.objects.all().order_by('updated').values()
        query_list = []
        
        for query in queryset:
            if startDateTime < query['updated'].replace(tzinfo=None) and endDateTime > query['updated'].replace(tzinfo=None):
                
                query_list.append(query)
                
        context['amount'] = len(query_list)
        context['data'] = query_list
        return render(request, 'reporting/reportingCustomRange.html', context)




class CustomSentCallListSummaryView(generic.View):
    

    def get(self, request):    
        form = forms.CustomReportRange()
        context = {'form':form}    
        return render(request, 'reporting/reportingCustomRange.html', context)


    def post(self, request):
        
        form = forms.CustomReportRange()
        context = {'form':form}
        startDateTime = datetime.datetime.fromisoformat(request.POST.get('startDateTime'))
        endDateTime = datetime.datetime.fromisoformat(request.POST.get('endDateTime'))
        
        queryset = Sent_Call_List.objects.all().order_by('updated').values()
        query_list = []
        
        for query in queryset:
            if startDateTime < query['updated'].replace(tzinfo=None) and endDateTime > query['updated'].replace(tzinfo=None):
                
                query_list.append(query)
                
        context['amount'] = len(query_list)
        context['data'] = query_list
        generate(startDateTime, endDateTime)
        return render(request, 'reporting/reportingCustomRange.html', context)