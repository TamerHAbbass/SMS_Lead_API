from rest_framework import serializers
from .models import SMS_Lead_Data

class SMSLeadSerializer(serializers.ModelSerializer):

    class Meta:

        model = SMS_Lead_Data

        fields = [
            "Number",
            "Type",
            "Timezone", 
            "First",
            "Last",
            "Address", 
            "City",
            "State",
            "Zip",
            "PropertyID",
            "UploadDate",
            "SMSMessage1",
            # "SMSMessage2",
            # "SMSMessage3",
            # "SMSMessage4",
            "SMSStatus",
            "UploadedToVoiceCampaign",
            "ContactCallable",
            "ZipCodeAutomaticTimeZone",
            "CallRecordLastAttempt_Number",
            "CallRecordLastResult_Number",
            "CallRecordLastAgentWrapup_Number",
            "SmsLastAttempt_Number",
            "SmsLastResult_Number",
            "Callable_Number",
            "AutomaticTimeZone_Number",
            "sentSMSId"
            "queued"
        ]
