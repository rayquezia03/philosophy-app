from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scheduler/', views.agendar, name='agendar'),
    path('get_queue/', views.get_queue, name='get_queue'),
    path('complete_current_customer_service/', views.complete_current_customer_service, name='complete_current_customer_service'),
    path('complete_workday/', views.complete_workday, name='complete_workday'),
    path('get_queue_completed/', views.get_queue_completed, name='get_queue_completed'),
]
