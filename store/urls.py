from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home_Page, name="home_page"),
    path("about/", views.about_page, name="about_page"),
    path("contact/", views.contact_page, name="contact_page"),
    path("products/", views.product_page.as_view(), name="products_page"),
    path("products/<int:pk>/", views.product_details, name="Product_detail"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("category/<str:foo>/", views.Category_view, name="category_page"),
    path("add-to-cart/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path('cart/',views.cart_summary,name='cart_summary')
]
