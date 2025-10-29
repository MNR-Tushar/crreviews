from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cr.models import *
from userprofile.models import *

@staff_member_required
def admin_dashboard(request):

    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
   
    pending_count = Review.objects.filter(is_anonymous=True, is_approved=False).count()
    anonymous_reviews = Review.objects.filter(is_anonymous=True, is_approved=True).count()
    
   
    total_users = User.objects.count()
    users=User.objects.all().order_by('-created_at')


    total_crs = CrProfile.objects.count()
    crs=CrProfile.objects.all().order_by('-created_at')


    total_reviews = Review.objects.count()
    reviews=Review.objects.all().order_by('-created_at')


    univercities=University.objects.all().order_by('-created_at')
    total_universities = University.objects.count()
    private_universities = University.objects.filter(type='Private').count()
    public_universities = University.objects.filter(type='Public').count()
    univercities = University.objects.annotate(total_cr=Count('university_crs',distinct=True),total_review=Count('university_crs__cr_reviews',distinct=True),total_users=Count('university_user',distinct=True))


    departments=Department.objects.all().order_by('-created_at')
    total_departments = Department.objects.count()
    departments = Department.objects.annotate(total_cr=Count('department_crs',distinct=True),total_review=Count('department_crs__cr_reviews',distinct=True),total_users=Count('department_user',distinct=True))


    pending = Review.objects.filter(is_anonymous=True, is_approved=False).order_by('-created_at')
    
    paginator = Paginator(pending, 10)
    page_number = request.GET.get('page', 1)
    
    try:
        pending = paginator.page(page_number)
    except PageNotAnInteger:
        pending = paginator.page(1)
    except EmptyPage:
        pending = paginator.page(1)
 
    
    context = {
        'pending_count': pending_count,
        'anonymous_reviews': anonymous_reviews,
        'total_users': total_users,
        'total_crs': total_crs,
        'total_reviews': total_reviews,
        'total_universities': total_universities,
        'total_departments': total_departments,
        'users':users,
        'crs':crs,
        'reviews':reviews,
        'univercities':univercities,
        'departments':departments,
        'private_universities':private_universities,
        'public_universities':public_universities,
        'pending_reviews': pending,
        'paginator': paginator,
       
    }
    
    return render(request, 'admin_dashboard/admin_dashboard.html', context)

