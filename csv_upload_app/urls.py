from django.urls import path
from . import views

urlpatterns = [
    path('upload-csv/', views.CSVUploadView.as_view(), name='upload_csv'),
]
