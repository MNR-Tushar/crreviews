from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')

def all_cr(request):
    return render(request,'all_cr.html')

def latest_reviews(request):
    return render(request,'latest_reviews.html')

def profile(request):
    return render(request,'profile.html')