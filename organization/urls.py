from django.urls import path
from . import views

app_name = 'organizations'
urlpatterns = [
    path('all/', views.ViewOrganizationsList.as_view(), name='list-of-organizations'),
    path('detail/<str:slug>', views.ViewOrganizationDetail.as_view(), name='detail-of-organization'),
    path('edit/<str:slug>', views.ViewEditOrganization.as_view(), name='edit-organization'),
    path('create/', views.ViewCreateOrganization.as_view(), name='create-organization'),
]
