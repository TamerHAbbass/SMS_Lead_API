import csv
from io import StringIO
from django.core.mail import EmailMessage


def build_report(success_list, call_list):

    rows = []
    csvfile = StringIO()
    fieldnames = list(rows[0].keys())

    for query in success_list:
        rows.append({
        "cl_uuid": query.cl_uuid,
        "Number": query.Number,
        "Type": query.Type,
        "Timezone": query.Timezone,
        "First": query.First,
        "Last": query.Last,
        "Address": query.Address,
        "City": query.City,
        "State": query.State,
        "Zip": query.Zip,
        "PropertyID": query.PropertyID,
        "UploadDate": query.UploadDate,
        "SMSMessage1": query.SMSMessage1,
        "SMSStatus": query.SMSStatus,
        "SMSTimeStamp": query.SMSTimeStamp,
        "UploadedToVoiceCampaign": query.UploadedToVoiceCampaign,
        "ContactCallable": query.ContactCallable,
        "UploadedToVoiceCampaign": query.UploadedToVoiceCampaign,
        "ZipCodeAutomaticTimeZone": query.ZipCodeAutomaticTimeZone,
        "CallRecordLastAttempt_Number": query.CallRecordLastAttempt_Number,
        "CallRecordLastResult_Number": query.CallRecordLastResult_Number,
        "CallRecordLastAgentWrapup_Number": query.CallRecordLastAgentWrapup_Number,
        "SmsLastAttempt_Number": query.SmsLastAttempt_Number,
        "SmsLastResult_Number": query.SmsLastResult_Number,
        "Callable_Number": query.Callable_Number,
        "AutomaticTimeZone_Number": query.AutomaticTimeZone_Number,
        "sentSMSId": query.sentSMSId,
        "queued": query.queued,
        })

    rows.append({
        'Total Successful Messages': str(len(rows))
    })

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

    return csvfile


def send_report_email(csvfile_success, csvfile_call_list):
    email = EmailMessage(
        'Report',
        'Body',
        'from@email.com',
        ['to@email.com'],
        )

    email.attach('SMS_API_Zillow_Campaign_Successful.csv', csvfile_success.getvalue(), 'text/csv')
    email.attach('SMS_API_Zillow_Campaign_Call_List.csv', csvfile_call_list.getvalue(), 'text/csv')
    email.send()