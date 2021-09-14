from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponse
from django.views import generic

from sms_lead.models import Sent_Call_List, SMS_Successful, Campaign
import datetime


class CreateCampaign(generic.View):

    def post(self, request):
        print(dir(request))
        c = Campaign()
        c.name = request.data['name']
        c.Call_List_ID = request.data['Call_List_ID']
        c.zillow_list_id = request.data['zillow_list_id']
        c.start = request.data['start']
        c.end = request.data['end']
        c.freaquency_seconds = request.data['freaquency_seconds']
        c.freaquency_minutes = request.data['freaquency_minutes']
        c.freaquency_hours = request.data['freaquency_hours']
        c.download_freaquency_minutes = request.data['download_freaquency_minutes']
        c.purecloud_client_id = request.data['purecloud_client_id']
        c.purecloud_client_secret = request.data['purecloud_client_secret']
        c.save()

        return c.uuid

