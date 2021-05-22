from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register/', views.RegisterPage, name="register"),
    path('', views.LoginPage, name="login"),
    path('home/', views.home, name="home"),
    path('logout/', views.LogoutUser, name="logout"),
    path('home/vcanteen/', views.vcanteen, name="vcanteen"),
    path('home/vlounge/', views.vlounge, name="vlounge"),
    path('update-item/', views.updateItem, name="update-item"),
    path('home/vcanteen/cart/', views.Cart, name="cart"),
    path('success/', views.success, name="success"),
    path('home/change-password/', views.change_password, name="change-password"),
    path('order-status/', views.get_order_status, name="order-status"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)