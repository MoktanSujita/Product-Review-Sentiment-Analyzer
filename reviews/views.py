from django.shortcuts import render
from .models import Review  

# Create your views here.
def reviews_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews_list.html', {'reviews': reviews})