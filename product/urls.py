from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('all/', views.ViewListProducts.as_view(), name='list-products'),
]
