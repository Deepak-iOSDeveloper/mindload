from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log/', views.log_today, name='log_today'),
    path('history/', views.history, name='history'),
    path('log/<int:pk>/', views.log_detail, name='log_detail'),
    path('insights/', views.insights, name='insights'),
    path('api/quick-log/', views.api_quick_log, name='api_quick_log'),
    path('api/chart-data/', views.api_chart_data, name='api_chart_data'),
]
