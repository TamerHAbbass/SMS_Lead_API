from django.urls import path
from django.conf.urls import url
from .views import CreateCampaign


urlpatterns = [
    path('create-campaign/', CreateCampaign.as_view()),
]