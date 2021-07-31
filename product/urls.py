from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('all/', views.ProductListView.as_view(), name='list-products'),
]
