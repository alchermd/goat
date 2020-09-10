from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_list, name='list_list'),
    path('<list_id>/', views.list_detail, name='list_detail'),
    path('<list_id>/new_item/', views.list_new_item, name='list_new_item'),
]
