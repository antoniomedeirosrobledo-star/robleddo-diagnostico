from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('claude/', views.claude_proxy, name='claude_proxy'),
    path('save-report/', views.save_report, name='save_report'),
    path('report/<str:uid>/', views.view_report, name='view_report'),
]
