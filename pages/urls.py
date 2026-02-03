from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('about/', views.about, name='about'),
    # Dynamic case study detail page
    path('case/<slug:slug>/', views.case_study_detail, name='case-detail'),
]
