from django.urls import path
from . import views

app_name = 'quote'
urlpatterns = [
    path('create/', views.QuoteCreateView.as_view(), name='create-quote'),
    path('all/', views.QuoteListView.as_view(), name='list-quotes'),
    path('detail/<str:pk>', views.QuoteDetailView.as_view(), name='detail-quotes'),
    path('pdf/<str:pk>', views.QuoteGetPDF.as_view(), name='pdf-quotes'),
    path('send/email/<str:pk>', views.send_email, name='send-email'),
]
