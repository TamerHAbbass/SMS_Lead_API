from django.db import models
import uuid
from django.conf import settings
from django.db.models.fields import DateTimeField
from rest_framework import serializers

class SMS_Lead_Data(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    cl_uuid = models.CharField(max_length=255, blank=True, null=True)
    Number = models.CharField(max_length=12, db_index=True)
    Type = models.CharField(max_length=20, db_index=True)
    Timezone = models.CharField(max_length=80, db_index=True)
    First = models.CharField(max_length=100, db_index=True)
    Last = models.CharField(max_length=100, db_index=True)
    Address = models.CharField(max_length=254, db_index=True)
    City = models.CharField(max_length=254, db_index=True)
    State = models.CharField(max_length=254, db_index=True)
    Zip = models.CharField(max_length=254, db_index=True)
    PropertyID = models.CharField(max_length=254, db_index=True)
    UploadDate = models.CharField(max_length=254, db_index=True)
    SMSMessage1 = models.CharField(max_length=511, db_index=True)
    # SMSMessage2 = models.CharField(max_length=511, db_index=True)
    # SMSMessage3 = models.CharField(max_length=511, db_index=True)
    # SMSMessage4 = models.CharField(max_length=511, db_index=True)
    SMSStatus = models.BooleanField(default=False, blank=True)
    SMSTimeStamp = models.CharField(max_length=100,blank=True, null=True)
    UploadedToVoiceCampaign = models.CharField(max_length=255,blank=True, db_index=True)
    ContactCallable = models.CharField(max_length=255,blank=True, db_index=True)
    UploadedToVoiceCampaign = models.CharField(max_length=255,blank=True, db_index=True)
    ZipCodeAutomaticTimeZone = models.CharField(max_length=255,blank=True, db_index=True)
    CallRecordLastAttempt_Number = models.CharField(max_length=255,blank=True, db_index=True)
    CallRecordLastResult_Number = models.CharField(max_length=255,blank=True, db_index=True)
    CallRecordLastAgentWrapup_Number = models.CharField(max_length=255,blank=True, db_index=True)
    SmsLastAttempt_Number = models.CharField(max_length=255,blank=True, db_index=True)
    SmsLastResult_Number = models.CharField(max_length=255,blank=True, db_index=True)
    Callable_Number = models.CharField(max_length=255,blank=True, db_index=True)
    AutomaticTimeZone_Number = models.CharField(max_length=255,blank=True, db_index=True)
    sentSMSId = models.UUIDField(db_index=True, null=True)
    queued = models.BooleanField(default=True, db_index=True)
    

    class Meta:

        abstract=True
        

class SMS_Queued(SMS_Lead_Data):
    updated = models.DateTimeField(auto_now=True, verbose_name="Last Modified", db_index=True)


class Sent_Call_List(SMS_Lead_Data):
    updated = models.DateTimeField(auto_now=True, verbose_name="Last Modified", db_index=True)


class SMS_Successful(SMS_Lead_Data):
    updated = models.DateTimeField(auto_now=True, verbose_name="Last Modified", db_index=True)



