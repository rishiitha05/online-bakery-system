from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    path('cart/', views.cart, name='cart'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),

    path('add-to-cart/<int:cake_id>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-wishlist/<int:cake_id>/',views.add_to_wishlist,name='add_to_wishlist'),

    path('increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-from-wishlist/<int:wishlist_id>/',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('logout/', views.logout_view, name='logout'),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
]