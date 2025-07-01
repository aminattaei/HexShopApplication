from django.contrib import admin
from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register("products", views.ProductListAPI)

urlpatterns = [
    # <---START BASE URLS AREA--->
    path("", views.Home_Page, name="home_page"),
    path("about/", views.about_page, name="about_page"),
    path("contact/", views.contact_page, name="contact_page"),
    path("products/", views.product_list, name="products_page"),
    path("products/<int:pk>/", views.product_details, name="Product_detail"),
    path("products/<int:pk>/delete/", views.delete_cart_item, name="cart_item_delete"),
    path("products/<int:pk>/update/", views.update_cart_item, name="Update_cart_item"),
    path("payment/<int:order_id>/", views.payment_view, name="payment"),
    path("shipping/", views.shipping_view, name="shipping-info"),
    # <---END BASE URLS AREA --->
    # <---START OPERATION URLS --->
    path("register/", views.register_view, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("category/<str:foo>/", views.Category_view, name="category_page"),
    path("add-to-cart/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_summary, name="cart_summary"),
    path("submit-comment/<int:pk>/", views.submit_comment_view, name="submit_comment"),
    # <---END OPERATION URLS --->
    # <---START API URLS --->
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # <---END API URLS --->
    # <---START API SCHEMA AREA--->
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # <---END API SCHEMA AREA--->
]
