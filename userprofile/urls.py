from django.urls import path
from .views import *

urlpatterns = [
    path('login/',login,name="login"),
    path('registration/',registration,name="registration"),
    path('logout/',logout,name="logout"),
    path('user_dashboard/',user_dasboard,name="user_dashboard"),
    path('admin_dashboard/',admin_dashboard,name="admin_dashboard"),
]
