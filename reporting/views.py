from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.views import generic
import json
from sms_lead.models import Sent_Call_List, SMS_Successful
from . import forms
import datetime


class DailySMSSuccessSummaryView(generic.View):

    def get(self, request):
        queryset = SMS_Successful.objects.all().order_by('updated').values()
        query_list = []
        context = {
            'amount': len(query_list),
            'data': []
            }
        for query in queryset:
            if (datetime.datetime.now() - datetime.timedelta(hours=24)) < query['updated'].replace(tzinfo=None) and datetime.datetime.now() > query['updated'].replace(tzinfo=None):
                context['data'][query['cl_uuid']] = {
                    'Number': query['Number'],
                    'Type': query['Type'],
                    'Timezone': query['Timezone'],
                    'First': query['First'],
                    'Last': query['Last'],
                    'Address': query['Address'],
                    'City': query['City'],
                    'State': query['State'],
                    'Zip': query['Zip'],
                    'PropertyID': query['PropertyID'],
                    'SMSMessage1': query['SMSMessage1']
                    }
            


        return render(request, 'reporting/reportingCustomRange.html', context)


class WeeklySMSSuccessSummaryView(generic.View):

    def get(self, request):
        queryset = SMS_Successful.objects.all().order_by('updated').values()
        query_list = []
        for query in queryset:
            if (datetime.datetime.now() - datetime.timedelta(weeks=1)) < query['updated'].replace(tzinfo=None) and datetime.datetime.now() > query['updated'].replace(tzinfo=None):
                query_list.append(query)
        
        for query in query_list:
            context = {
                'amount': len(query_list),
                'data': [{
                    'cl_uuid': query['cl_uuid'],
                    'Number': query['Number'],
                    'Type': query['Type'],
                    'Timezone': query['Timezone'],
                    'First': query['First'],
                    'Last': query['Last'],
                    'Address': query['Address'],
                    'City': query['City'],
                    'State': query['State'],
                    'Zip': query['Zip'],
                    'PropertyID': query['PropertyID'],
                    'SMSMessage1': query['SMSMessage1']
                    }]
                }

        return HttpResponse(str(len(query_list)), content_type='application/json')


class MonthlySMSSuccessSummaryView(generic.View):

    def get(self, request):
        queryset = SMS_Successful.objects.all().order_by('updated').values()
        query_list = []
        context = {
            'data': []
            }
        print(type(context['data']))
        for query in queryset:
            
            if (datetime.datetime.now() - datetime.timedelta(weeks=4)) < query['updated'].replace(tzinfo=None) and datetime.datetime.now() > query['updated'].replace(tzinfo=None):
                query_list.append(
                    {
                        'cl_uuid': query['cl_uuid'],
                        'Number': query['Number'],
                        'Type': query['Type'],
                        'Timezone': query['Timezone'],
                        'First': query['First'],
                        'Last': query['Last'],
                        'Address': query['Address'],
                        'City': query['City'],
                        'State': query['State'],
                        'Zip': query['Zip'],
                        'PropertyID': query['PropertyID'],
                        'SMSMessage1': query['SMSMessage1'],
                        'updated': query['updated']
                    })
        
        context['data'] = query_list
        context['amount'] = len(query_list),
        print(context['data'])
        return render(request, 'reporting/reportingCustomRange.html', context)


class CustomSMSSuccessSummaryView(generic.View):


    def get(self, request):    
        form = forms.CustomReportRange()
        context = {'form':form}    
        return render(request, 'reporting/reportingCustomRange.html', context)


    def post(self, request):
        startDateTime = datetime.datetime.fromisoformat(request.POST.get('startDateTime'))
        endDateTime = datetime.datetime.fromisoformat(request.POST.get('endDateTime'))
        
        queryset = SMS_Successful.objects.all().order_by('updated').values()
        query_list = []
        
        for query in queryset:
            if startDateTime < query['updated'].replace(tzinfo=None) and endDateTime > query['updated'].replace(tzinfo=None):
                query_list.append(query)
                form = forms.CustomReportRange()

                for query in query_list:
                    context = {
                        'form':form,
                        'amount': len(query_list),
                        'data': [{
                            'cl_uuid': query['cl_uuid'],
                            'Number': query['Number'],
                            'Type': query['Type'],
                            'Timezone': query['Timezone'],
                            'First': query['First'],
                            'Last': query['Last'],
                            'Address': query['Address'],
                            'City': query['City'],
                            'State': query['State'],
                            'Zip': query['Zip'],
                            'PropertyID': query['PropertyID'],
                            'SMSMessage1': query['SMSMessage1']
                            }]
                        }

                return render(request, 'reporting/reportingCustomRange.html', context)
            else:
                return HttpResponse('No results')


class CustomSentCallListSummaryView(generic.View):
    

    def get(self, request):    
        form = forms.CustomReportRange()
        context = {'form':form}    
        return render(request, 'reporting/reportingCustomRange.html', context)


    def post(self, request):
        startDateTime = datetime.datetime.fromisoformat(request.POST.get('startDateTime'))
        endDateTime = datetime.datetime.fromisoformat(request.POST.get('endDateTime'))

        queryset = Sent_Call_List.objects.all().order_by('updated').values()
        query_list = []
        
        for query in queryset:
            if startDateTime < query['updated'].replace(tzinfo=None) and endDateTime > query['updated'].replace(tzinfo=None):
                query_list.append(query)
                form = forms.CustomReportRange()
            
                context = {
                    'form':form,
                    'amount': len(query_list),
                    'data': query_list
                    }

                return render(request, 'reporting/reportingCustomRange.html', context)
            else:
                return HttpResponse('No results')