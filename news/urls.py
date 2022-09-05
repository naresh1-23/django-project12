from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('useradmin/', views.useradmin, name = 'user-admin'),
    path('query/', views.userquery , name = 'user-query'),
    path('singlepaymentuser/<int:id>', views.singlepayment, name = 'singlepayment-user')
]