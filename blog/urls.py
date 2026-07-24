from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_view, name='index'),
    path('<int:case_id>/', views.case_detail_view, name='case_detail'),
]