from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/store/create/', views.create_store, name='create_store'),
    path('vendor/store/<int:store_id>/edit/', views.edit_store, name='edit_store'),
    path('vendor/store/<int:store_id>/delete/', views.delete_store, name='delete_store'),
    path('vendor/store/<int:store_id>/products/', views.store_products, name='store_products'),
    path('vendor/store/<int:store_id>/product/add/', views.add_product, name='add_product'),
    path('vendor/product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('vendor/product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/add/', views.add_review, name='add_review'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
]