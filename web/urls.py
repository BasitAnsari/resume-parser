from django.urls import path

from . import views
from .views import DeleteView

urlpatterns = [
    path('', views.home, name='web-home'),
    path('resume/<str:pk>/', views.ResumeWebDetail, name = 'web-detail'),
    path('resume/parse/<str:pk>/', views.ResumeParse, name = 'web-parse'),
    path('resume/<str:pk>/delete/', DeleteView.as_view(), name = 'web-delete'),
    path('resume/excel/view/', views.ResumeExcel, name = 'to-excel'),
    #path('resume/<str:pk>/delete/', views.ResumeWebDelete, name = 'web-delete'),
]