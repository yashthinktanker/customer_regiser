from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path('',views.home,name="home"),
    path('login',views.login,name="login"),
    # path('otp', views.otp_verify, name='otp'),
    path('otp2', views.otp_verify2, name='otp2'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
]
