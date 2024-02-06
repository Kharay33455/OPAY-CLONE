from django.urls import path
from . import views



app_name = 'users'

urlpatterns = [
    path('login/', views.login_request, name='login'),
    path('register/', views.registration_request, name = 'register'),
    path('logout/', views.logout_request, name = 'logout'),
    
]