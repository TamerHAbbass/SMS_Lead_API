from django.urls import path
from . import views


urlpatterns = [
    path('daily/', views.DailySMSSuccessSummaryView.as_view(), name="daily"),
    path('weekly/', views.WeeklySMSSuccessSummaryView.as_view(), name="weekly"),
    path('monthly/', views.MonthlySMSSuccessSummaryView.as_view(), name="monthly"),
    path('custom/successful/', views.CustomSMSSuccessSummaryView.as_view(), name="custom_successful"),
    path('custom/calllist/', views.CustomSentCallListSummaryView.as_view(), name="custom_calllist")
]
