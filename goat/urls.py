from django.urls import path, include
from lists import views

urlpatterns = [
    path('', views.home_page),
    path('lists/', include('lists.urls')),
]
