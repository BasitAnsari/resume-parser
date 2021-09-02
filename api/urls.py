from django.urls import path
from . import views

urlpatterns = [
    path('resume-create/', views.ResumeCreate, name = 'resume-create'),
    path('resume-detail/<str:pk>/', views.ResumeDetail, name = 'resume-parse'),
    path('resume-list/', views.ResumeList, name = 'resume-list'),
    path('resume-parse/<str:pk>/', views.ResumeParse, name = 'resume-parse'),
    path('resume-delete/<str:pk>/', views.ResumeDelete, name = 'resume-delete'),
]