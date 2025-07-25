from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest

from .forms import ContactForm, CommentForm, ShippingAddressForm
from .models import (
    Product,
    Category,
    Cart,
    CartItem,
    Customer,
    Comment,
    Order,
    OrderItem,
)
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

    """
    Handles the shipping address form submission and order creation process.

    This view is responsible for processing the shipping address form submitted by a logged-in user.
    It performs the following steps:

    1. Validates the form data submitted via POST.
    2. Retrieves the currently logged-in user's `Customer` profile.
    3. Checks if the user's shopping cart exists and contains items.
    4. Creates a new `Order` instance with the submitted shipping address and user's phone number.
    5. Iterates over each item in the user's cart and creates corresponding `OrderItem` entries.
    6. Assigns the newly created order to the shipping address instance and saves it.
    7. Clears all items from the user's cart (emptying it).
    8. Redirects the user to the payment page with the newly created order ID.

    If the form is invalid or the cart is empty, appropriate error messages are shown to the user,
    and they are redirected accordingly.

    GET requests simply render the empty shipping form.

    Access Control:
    - This view is protected by login. Only authenticated users can access it.

    Context:
    - On GET: renders `cart/shipping.html` with an empty `ShippingAddressForm`.
    - On POST (valid): redirects to "payment" view.
    - On POST (invalid): re-renders form with error messages.

    Raises:
        Http404: if customer or cart not found (handled via error messages and redirects).
    """

    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.filter(email=request.user.email).first()
            if not customer:
                messages.error(request, "Customer profile not found.")
                return redirect("home_page")

            cart = Cart.objects.filter(customer=customer).first()
            if not cart or not cart.items.exists():
                messages.error(request, "Shopping cart is empty or not found.")
                return redirect("cart")

            shipping = form.save(commit=False)
            shipping.customer = customer

            order = Order.objects.create(
                customer=customer,
                address=shipping.address,
                phone=customer.phone,
                status=False,
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order, product=item.product, quantity=item.quantity
                )

            shipping.order = order
            shipping.save()

            cart.items.all().delete()

            return redirect("payment", order_id=order.id)
        else:
            messages.error(request, "Form is not valid. Please check the fields.")
    else:
        form = ShippingAddressForm()

    return render(request, "cart/shipping.html", {"form": form})


@login_required(login_url="/store/login/")
def payment_view(request, order_id):
    """
    Handles the confirmation or cancellation of an order payment.

    This view allows an authenticated user to either confirm or cancel the payment of a specific order.
    The `order_id` is used to retrieve the relevant `Order` object.

    Functionality:
    1. If the request method is POST:
        - If the user clicks the "Confirm" button:
            * The order's status is updated to True (indicating the order is paid).
            * A success message is displayed.
            * User is redirected to the home page.
        - If the user clicks the "Cancel" button:
            * The order remains unpaid.
            * A warning message is displayed.
            * User is redirected back to the cart summary page.

    2. If the request method is GET:
        - Renders the `cart/payment.html` template with the order details for user confirmation.

    Access Control:
    - Only authenticated users can access this view.

    Arguments:
    - request: HttpRequest object.
    - order_id: ID of the order to be confirmed or canceled.

    Context:
    - 'order': The order object corresponding to the provided `order_id`.

    Templates:
    - cart/payment.html: Displayed to the user for confirming/canceling the payment.

    Raises:
    - Http404: If no Order object is found with the given `order_id`.
    """

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        if "confirm" in request.POST:
            order.status = True
            order.save()
            messages.success(request, "Payment completed successfully ✅")
            return redirect("home_page")
        elif "cancel" in request.POST:
            messages.warning(request, "Payment cancelled ❌")
            return redirect("cart_summary")
    return render(request, "cart/payment.html", {"order": order})
