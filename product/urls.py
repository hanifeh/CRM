from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('all/', views.ViewProductsList.as_view(), name='list-of-products'),
]
