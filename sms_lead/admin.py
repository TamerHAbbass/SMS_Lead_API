from django.contrib import admin
from .models import SMS_Queued, Sent_Call_List, SMS_Successful
# Register your models here.


admin.site.register(SMS_Queued)
admin.site.register(Sent_Call_List)
admin.site.register(SMS_Successful)