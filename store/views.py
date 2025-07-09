from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest

from .forms import ContactForm, CommentForm, ShippingAddressForm
from .models import Product, Category, Cart, CartItem, Customer, Comment, Order
from .serializers import ProductSerializer

from rest_framework.viewsets import ModelViewSet

from decimal import Decimal


class ProductListAPI(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


def Home_Page(request):
    """
    Render the home page with products categorized by gender/age.
    """
    mensProduct = Product.objects.filter(category__name="men")
    womensProduct = Product.objects.filter(category__name="women")
    kidsProduct = Product.objects.filter(category__name="kids")

    return render(
        request,
        "Index/index.html",
        {
            "mensProduct": mensProduct,
            "womensProduct": womensProduct,
            "kidsProduct": kidsProduct,
        },
    )


def about_page(request):
    """Render static about page."""
    return render(request, "Index/about.html")


def contact_page(request):
    """Render static contact page (fallback)."""
    return render(request, "Index/contact.html")


def product_list(request):
    products = Product.objects.all()
    return render(request, "Index/products.html", {"products": products})


def product_details(request, pk):
    """
    Display product details, related products and comments.
    """
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[
        :6
    ]
    comments = Comment.objects.filter(product=product).order_by("-created_at")

    return render(
        request,
        "Index/single-product.html",
        {
            "product": product,
            "comments": comments,
            "Related_Products": related_products,
        },
    )


def register_view(request):
    """
    Handle user registration.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(
                first_name=user.username,
                email=user.email,
            )
            print(user)
            login(request, user)
            messages.success(request, "Your account was successfully created!")
            return redirect("home_page")
        messages.error(request, "Invalid registration information.")
        return redirect("register")

    return render(request, "registration/signup.html", {"form": UserCreationForm()})


def logout_user(request):
    """Log out the current user."""
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("home_page")


def login_user(request):
    """
    Handle user login.
    """
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect("home_page")
        messages.error(request, "Username or Password is incorrect.")
        return redirect("login")

    return render(request, "registration/login.html")


def Contact_View(request):
    """
    Handle contact form submission.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message was successfully sent.")
            return redirect("home_page")
        messages.error(request, "Error sending your message. Try again.")
        return redirect("contact_page")

    return render(request, "Index/contact.html", {"form": ContactForm()})


@login_required(login_url="/store/login/")
def Category_view(request, foo):
    """
    Display products in a specific category.
    """
    foo = foo.replace(" ", "-").lower()
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(
            request, "Index/category.html", {"products": products, "category": category}
        )
    except Category.DoesNotExist:
        messages.error(request, "This category does not exist...")
        return redirect("home_page")


@login_required(login_url="/store/login/")
def add_to_cart(request, pk):
    """
    Add a product to the user's cart.
    """
    product = get_object_or_404(Product, pk=pk)
    customer = Customer.objects.filter(email=request.user.email).first()
    if not customer:
        messages.error(request, "Customer profile not found.")
        return redirect("home_page")

    cart, _ = Cart.objects.get_or_create(customer=customer)
    quantity = int(request.POST.get("quantity", 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity = quantity if created else cart_item.quantity + quantity
    cart_item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect("Product_detail", pk=pk)


@login_required(login_url="/store/login/")
def delete_cart_item(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Deletes a specific product from the authenticated user's shopping cart.
    """

    product = get_object_or_404(Product, pk=pk)

    customer = Customer.objects.filter(email=request.user.email).first()
    if not customer:
        messages.error(request, "Customer not found.")
        return redirect("home_page")

    cart = Cart.objects.filter(customer=customer).first()
    if not cart:
        messages.error(request, "Shopping cart not found.")
        return redirect("home_page")

    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if not cart_item:
        messages.error(request, "Item not found in your cart.")
        return redirect("home_page")

    cart_item.delete()
    messages.success(request, f"{ product.name } successfully removed from your cart.")
    return redirect("cart_summary")


@login_required(login_url="/store/login/")
def update_cart_item(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Updates a specific product from the authenticated user's shopping cart.
    """

    product = get_object_or_404(Product, pk=pk)
    customer = Customer.objects.filter(email=request.user.email).first()

    if not customer:
        messages.error(request, "Customer not found.")
        return redirect("home_page")

    cart = Cart.objects.filter(customer=customer).first()
    if not cart:
        messages.error(request, "Shopping cart not found.")
        return redirect("home_page")

    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if not cart_item:
        messages.error(request, "Item not found in your cart.")
        return redirect("home_page")

    try:
        new_quantity = int(request.POST.get("new_quantity"))
    except (TypeError, ValueError):
        messages.error(request, "Invalid quantity value.")
        return redirect("Product_detail", pk=pk)

    if cart_item.quantity != new_quantity:
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, "Cart item updated successfully.")
    else:
        messages.info(request, "Quantity is already up to date.")

    return redirect("Product_detail", pk=pk)


@login_required(login_url="/store/login/")
def cart_summary(request):
    """
    Display the current user's cart summary.
    """
    customer = Customer.objects.filter(email=request.user.email).first()
    if not customer:
        messages.error(request, "Customer profile not found.")
        return redirect("home_page")

    cart = Cart.objects.filter(customer=customer).first()

    if cart:
        items = cart.items.all()
        total = cart.get_total_price()
        tax = round(total * Decimal("0.09"), 2)
        shipping = Decimal("5.00")
        grand_total = total + tax + shipping
    else:
        items = []
        total = Decimal("0.00")
        tax = Decimal("0.00")
        shipping = Decimal("0.00")
        grand_total = Decimal("0.00")

    return render(
        request,
        "cart/cart_summary.html",
        {
            "items": items,
            "total": total,
            "tax": tax,
            "shipping": shipping,
            "grand_total": grand_total,
        },
    )


@login_required(login_url="/store/login/")
def submit_comment_view(request, pk):
    """
    Handle comment submission on product detail page.
    """
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            product = get_object_or_404(Product, pk=pk)
            customer = Customer.objects.filter(email=request.user.email).first()
            if not customer:
                messages.error(request, "Customer profile not found.")
                return redirect("home_page")

            comment = form.save(commit=False)
            comment.product = product
            comment.customer = customer
            comment.save()

            messages.success(request, "Your comment was successfully submitted.")
            return redirect("Product_detail", pk=pk)

        messages.error(request, "There was a problem submitting your comment.")
        return redirect("Product_detail", pk=pk)

    return redirect("home_page")


@login_required(login_url="/store/login/")
def shipping_view(request):
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            queryset = form.save(commit=False)
            customer = Customer.objects.filter(email=request.user.email).first()
            if not customer:
                messages.error(request, "Customer profile not found.")
                return redirect("home_page")

            cart = Cart.objects.filter(customer=customer).first()
            if not cart:
                messages.error(request, "Shopping cart not found.")
                return redirect("home_page")

            queryset.customer = customer
            queryset.order = Order.objects.get(customer=customer)
            queryset.save()
        else:
            messages.error(request, "Form not valid please check fields")
            return redirect("home_page")
    else:
        form = ShippingAddressForm()
    
    cart.delete()
    messages.success(request, "Shipping information saved. Your shopping cart will be delivered to you soon.")
    return redirect("home_page")
