from django.urls import path
from . import views

urlpatterns = [
    path('do_task', views.do_task),
    path('get_a_task', views.get_a_task),
    path('do_auto_reset', views.do_auto_reset),
]
