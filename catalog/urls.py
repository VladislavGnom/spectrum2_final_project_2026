from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog_view, name='index'),
    path('<slug:slug>/', views.robot_detail_view, name='robot_detail'),
]