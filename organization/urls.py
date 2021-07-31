from django.urls import path
from . import views

app_name = 'organizations'
urlpatterns = [
    path('all/', views.OrganizationsListView.as_view(), name='list-organizations'),
    path('detail/<str:slug>', views.OrganizationDetailView.as_view(), name='detail-organization'),
    path('edit/<str:slug>', views.OrganizationEditView.as_view(), name='edit-organization'),
    path('create/', views.OrganizationCreateView.as_view(), name='create-organization'),
]
