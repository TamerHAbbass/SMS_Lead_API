from django.urls import path
from .views import SMSLeadListAPIView, SMSLeadDetailAPIView


urlpatterns = [
    path('lead/', SMSLeadListAPIView.as_view(), name="list"),
    path('leads/', SMSLeadDetailAPIView.as_view(), name="detail"),
]