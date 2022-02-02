from django.test import TestCase

# Create your tests here.

for i in contacts_list:
    S.uuid = i.uuid
    S.campaign = i.campaign
    S.cl_uuid = i.cl_uuid
    S.Number = i.Number
    S.Type = i.Type
    S.Timezone = i.Timezone
    S.First = i.First
    S.Last = i.Last
    S.Address = i.Address
    S.City = i.City
    S.State = i.State
    S.Zip = i.Zip
    S.PropertyID = i.PropertyID
    S.UploadDate = i.UploadDate
    S.SMSMessage1 = i.SMSMessage1
    S.SMSStatus = i.SMSStatus
    S.SMSTimeStamp = i.SMSTimeStamp
    S.UploadedToVoiceCampaign = i.UploadedToVoiceCampaign
    S.ContactCallable = i.ContactCallable
    S.UploadedToVoiceCampaign = i.UploadedToVoiceCampaign
    S.ZipCodeAutomaticTimeZone = i.ZipCodeAutomaticTimeZone
    S.CallRecordLastAttempt_Number = i.CallRecordLastAttempt_Number
    S.CallRecordLastResult_Number = i.CallRecordLastResult_Number
    S.CallRecordLastAgentWrapup_Number = i.CallRecordLastAgentWrapup_Number
    S.SmsLastAttempt_Number = i.SmsLastAttempt_Number
    S.SmsLastResult_Number = i.SmsLastResult_Number
    S.Callable_Number = i.Callable_Number
    S.AutomaticTimeZone_Number = i.AutomaticTimeZone_Number
    S.sentSMSId = i.sentSMSId
    S.queued = i.queued
    S.save
    i.delete()
