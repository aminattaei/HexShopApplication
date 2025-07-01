from django.contrib import admin
from .models import (
    Category,
    Customer,
    Product,
    Order,
    OrderItem,
    Contact,
    Comment,
    ShippingAddress,
    Cart,
    CartItem,
)


# --------------------
# Category Admin
# --------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


# --------------------
# Customer Admin
# --------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "phone"]
    search_fields = ["first_name", "last_name", "email"]
    list_filter = ["email"]


# --------------------
# Product Admin
# --------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "category", "is_sale", "sale_price"]
    list_filter = ["is_sale", "category"]
    search_fields = ["name", "description"]
    list_editable = ["price", "is_sale", "sale_price"]


# --------------------
# Order Item Inline
# --------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# --------------------
# Order Admin
# --------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "date", "status"]
    list_filter = ["status", "date"]
    search_fields = ["customer__first_name", "customer__last_name"]
    inlines = [OrderItemInline]


# --------------------
# Contact Admin
# --------------------
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["fullname", "email"]
    search_fields = ["fullname", "email"]


# --------------------
# Comment Admin
# --------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["product", "customer", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["customer__first_name", "product__name"]


# --------------------
# Shipping Address Admin
# --------------------
admin.site.register(ShippingAddress)


# --------------------
# Cart Item Inline
# --------------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


# --------------------
# Cart Admin
# --------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "created_at", "is_active"]
    list_filter = ["is_active", "created_at"]
    inlines = [CartItemInline]


# --------------------
# Cart Item Admin
# --------------------
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity"]
    list_filter = ["cart"]
    search_fields = ["product__name"]
