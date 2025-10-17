from django.urls import path
from .views import *

urlpatterns = [
    path('login/',login,name="login"),
    path('registration/',registration,name="registration"),
    path('logout/',logout,name="logout"),
    path('user_dashboard/<str:slug>/',user_dasboard,name="user_dashboard"),
    path('view_profile/<str:slug>/',view_profile,name="view_profile"),
    path('user_view/<str:slug>/',user_view,name="user_view"),
    path('admin_dashboard/',admin_dashboard,name="admin_dashboard"),
    path('edit_user/<str:slug>/',edit_user,name="edit_user"),
    path('settings/',settings,name="settings"),
    path('save-cr/<str:slug>/', save_cr, name='save_cr'),
    path('remove-saved-cr/<str:slug>/', remove_saved_cr, name='remove_saved_cr'),
    # path('saved-crs/', saved_cr_list, name='saved_cr_list'),

]
