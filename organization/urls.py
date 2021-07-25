from django.urls import path
from . import views

app_name = 'organizations'
urlpatterns = [
    path('all/', views.ViewListOrganizations.as_view(), name='list-organizations'),
    path('detail/<str:slug>', views.ViewDetailOrganization.as_view(), name='detail-organization'),
    path('edit/<str:slug>', views.ViewEditOrganization.as_view(), name='edit-organization'),
    path('create/', views.ViewCreateOrganization.as_view(), name='create-organization'),
]
