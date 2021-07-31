from django.urls import path
from . import views

app_name = 'followup'
urlpatterns = [
    path('detail/<str:slug>', views.FollowUpDetailView.as_view(), name='detail-followup'),
    path('create/', views.FollowUpCreateView.as_view(), name='create-followup'),
]
