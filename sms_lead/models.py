from django.db import models
import uuid
from django.conf import settings

class SMS_Lead_Data(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    Number = models.CharField(max_length=12, db_index=True)
    Type = models.CharField(max_length=20, db_index=True)
    Timezone = models.CharField(max_length=80, db_index=True)
    First = models.CharField(max_length=100, db_index=True)
    Last = models.CharField(max_length=100, db_index=True)
    Address = models.CharField(max_length=254, db_index=True)
    City = models.CharField(max_length=254, db_index=True)
    State = models.CharField(max_length=254, db_index=True)
    Zip = models.CharField(max_length=254, db_index=True)
    # PropertyID = models.CharField(max_length=254, db_index=True)
    # UploadDate = models.CharField(max_length=254, db_index=True)
    # SMSMessage1 = models.CharField(max_length=511, db_index=True)
    # SMSMessage2 = models.CharField(max_length=511, db_index=True)
    # SMSMessage3 = models.CharField(max_length=511, db_index=True)
    # SMSMessage4 = models.CharField(max_length=511, db_index=True)
    # SMSStatus = models.BooleanField(default=False)
    # SMSTimeStamp = models.DateField(auto_now=True)

    def __int__(self):
        return self.uuid