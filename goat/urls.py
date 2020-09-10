from django.urls import path
from lists import views

urlpatterns = [
    path('', views.home_page),
    path('lists/', views.list_list, name='list_list'),
    path('lists/the-only-list-in-the-world/', views.list_detail, name='list_detail'),
]
