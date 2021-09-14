from django import forms
from sms_lead import models
import datetime

class CustomReportRange(forms.Form):

    startDateTime = forms.DateTimeField(initial=datetime.datetime.now)
    endDateTime = forms.DateTimeField(initial=datetime.datetime.now)

