from django.urls import path
from . import views

app_name = 'quote'
urlpatterns = [
    path('create/', views.ViewCreateQuote.as_view(), name='create-quote'),
    path('all/', views.ViewListQuote.as_view(), name='list-quotes'),
    path('detail/<str:pk>', views.ViewDetailQuote.as_view(), name='detail-quotes'),
    path('pdf/<str:pk>', views.GetPDFQuote.as_view(), name='pdf-quotes'),
    path('download/pdf/<str:pk>', views.DownloadPDFQuote.as_view(), name='download-pdf-quotes'),
    path('send/email/<str:pk>', views.send_email, name='send-email')
]
