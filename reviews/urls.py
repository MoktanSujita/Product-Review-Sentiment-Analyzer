from django.urls import path
from . import views

urlpatterns = [  

    path('', views.analyze_review, name='review_analysis'), 
    

]