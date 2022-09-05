from django.urls import path
from . import views
urlpatterns = [
    path('', views.adminhome , name = 'admin-home'),
    path('uploadpost/', views.UploadPost, name = 'admin-uploadpost'),
    path('Viewcomment/', views.Viewcomment, name = 'admin-viewcomment'),
    path('Viewpaymentdetail/', views.ViewPaymentDetail, name = 'admin-viewpayment'),
    path('single-payment/<int:id>/', views.singlepayment, name = 'singlepayment')
]