from django.urls import path

from . import views

urlpatterns=[
    path('',views.HomeView.as_view(),name='home'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('product/<int:id>/detail/', views.ProductDetailView.as_view(), name='product_detail'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('my-wishlist/', views.wishlist_view, name='wishlist_view'),
    path('cart/', views.cart_detail, name='cart_detail'),

]