from django.urls import path
from lists import views

urlpatterns = [
    path('', views.home_page),
    path('lists/', views.list_list, name='list_list'),
    path('lists/<list_id>/', views.list_detail, name='list_detail'),
    path('lists/<list_id>/new_item/', views.list_new_item, name='list_new_item'),
]
