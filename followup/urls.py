from django.urls import path
from . import views

app_name = 'followup'
urlpatterns = [
    path('detail/<str:slug>', views.ViewDetailFollowUp.as_view(), name='detail-followup'),
    path('createnew/', views.ViewCreateFollowUp.as_view(), name='create-followup'),
]
