from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ShopHome'),
    path('about/', views.about, name='About'),
    path('contact/', views.contact, name='Contact'),
    path('search/', views.search, name='Search'),
    path("products/<int:myid>", views.prodview, name='Product View'),
    path('checkout/', views.checkout, name='Checkout'),
    path('cart/', views.cart, name='Cart'),
    # path('cartupdate/', views.cartUpdate, name='Cart Update'),
    path('register/', views.RegisterForm.as_view(), name='Register'),
    path('login/', views.loginUser, name='Login'),
    path('logout/', views.logoutUser, name='LogoutUser'),
]