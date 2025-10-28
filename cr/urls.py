from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('all_cr/',all_cr,name='all_cr'),
    path('latest_reviews/',latest_reviews,name='latest_reviews'),
    path('cr_profile/<str:slug>/',cr_profile,name='cr_profile'),
    path('addcr/',add_cr,name='add_cr'),
    path('edit_cr/<str:slug>/',edit_cr_profile,name='edit_cr_profile'),
    path('delete_cr/<str:slug>/',delete_cr_profile,name='delete_cr_profile'),
    path('submit_review/<str:cr_slug>/',submit_review,name='submit_review'),
    path('edit_review/<str:slug>/',edit_review,name='edit_review'),
    path('delete_review/<str:slug>/',delete_review,name='delete_review'),


    path('review_status/pending-reviews/', pending_reviews, name='pending_reviews'),
    path('review_status/approve-review/<str:slug>/', approve_review, name='approve_review'),
    path('review_status/reject-review/<str:slug>/', reject_review, name='reject_review'),
]
