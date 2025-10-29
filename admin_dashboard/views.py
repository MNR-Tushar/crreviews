from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from cr.models import *
from userprofile.models import *

@staff_member_required
def admin_dashboard(request):

    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
   
    pending_count = Review.objects.filter(is_anonymous=True, is_approved=False).count()
    
   
    total_users = User.objects.count()
    total_crs = CrProfile.objects.count()
    total_reviews = Review.objects.count()
    total_universities = University.objects.count()
    total_departments = Department.objects.count()
    
    context = {
        'pending_count': pending_count,
        'total_users': total_users,
        'total_crs': total_crs,
        'total_reviews': total_reviews,
        'total_universities': total_universities,
        'total_departments': total_departments,
    }
    
    return render(request, 'admin_dashboard/admin_dashboard.html', context)