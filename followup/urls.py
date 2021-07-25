from django.urls import path
from . import views

app_name = 'followup'
urlpatterns = [
    path('create/<str:slug>', views.ViewCreateFollowUp.as_view(), name='create-followup'),
    path('detail/<str:slug>', views.ViewDetailFollowUp.as_view(), name='detail-followup'),
]
