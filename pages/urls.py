from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # Case study pages
    path('cases/angular-myflix/', views.angular_myflix_case, name='angular-myflix-case'),
    path('cases/meet-app/', views.meetapp_case, name='meetapp-case'),
    path('cases/pokemon/', views.pokemon_case, name='pokemon-case'),
    path('cases/promontolio/', views.promontolio_case, name='promontolio-case'),
    path('cases/myflix/', views.myflix_case, name='myflix-case'),
    path('cases/job-tracker/', views.jobtracker_case, name='jobtracker-case'),
]
