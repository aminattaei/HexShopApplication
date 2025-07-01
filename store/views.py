from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


from .forms import ContactForm,CommentForm
from .models import Product, Category, Cart, CartItem, Customer,Comment


def Home_Page(request):
    MensCategory = Category.objects.get(name="men")
    WomensCategory = Category.objects.get(name="women")
    KidssCategory = Category.objects.get(name="kids")

    mensProduct = Product.objects.filter(category=MensCategory)
    womensProduct = Product.objects.filter(category=WomensCategory)
    kidsProduct = Product.objects.filter(category=KidssCategory)

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
    return render(request, "Index/about.html", {})


def contact_page(request):
    return render(request, "Index/contact.html", {})


class product_page(generic.ListView):
    template_name = "Index/products.html"
    model = Product
    context_object_name = "products"


def product_details(request, pk):
    product = Product.objects.get(id=pk)
    comments = Comment.objects.filter(product=product).order_by('-created_at')

    context = {"product": product,'comments':comments}

    return render(request, "Index/single-product.html", context)


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(
                first_name=user.username,
                last_name="",
                email=user.email,
                password="",
            )
            messages.success(request, "Your account was successfully created!")
            login(request, user)
            return redirect("home_page")


def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("home_page")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect("home_page")
        else:
            messages.error(
                request,
                "Username or Password is Wrong! Please Retype username and password or Try Again Later.",
            )
            return redirect("login")
    else:
        return render(request, "registration/login.html", {})

# This Function is Not Ready...!!!
def Contact_View(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your message to our team has been successfully saved."
            )
            return redirect("home_page")
        else:
            messages.error(
                request,
                "There was a problem sending the message. Please try again.",
            )
            return redirect("contact_page")

    else:
        form = ContactForm()

    return render(request, "Index/contact.html", {"form": form})


@login_required(login_url="/store/login/")
def Category_view(request, foo: str):
    foo = foo.replace(" ", "-").lower()
    try:
        category = Category.objects.get(name=foo)

        products = Product.objects.filter(category=category)
        return render(
            request, "Index/category.html", {"products": products, "category": category}
        )
    except:
        messages.error(request, "This category does not exist... ")
        return redirect("home_page")


@login_required(login_url="/store/login/")
def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    user = request.user

    try:
        customer = Customer.objects.filter(email=user.email).first()
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect("home_page")

    cart, created = Cart.objects.get_or_create(customer=customer)

    quantity = int(request.POST.get("quantity", 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect("Product_detail", pk=pk)


@login_required(login_url="/store/login/")
def cart_summary(request):
    user = request.user

    try:
        customer = Customer.objects.filter(email=user.email).first()
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect("home_page")

    try:
        cart = Cart.objects.get(customer=customer)
        items = cart.items.all()
        total = cart.get_total_price()
    except Cart.DoesNotExist:
        items = []
        total = 0

    return render(
        request,
        "cart/cart_summary.html",
        {
            "items": items,
            "total": total,
        },
    )

@login_required(login_url="/store/login/")
def submit_comment_view(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            product = get_object_or_404(Product, pk=pk)
            customer = Customer.objects.filter(email=request.user.email).first()

            if not customer:
                messages.error(request, "Customer profile not found.")
                return redirect('home_page')

            comment = form.save(commit=False)
            comment.product = product
            comment.customer = customer
            comment.save()

            messages.success(request, "Your comment was successfully submitted.")
            return redirect('Product_detail', pk=pk)

        else:
            messages.error(request, "There was a problem submitting your comment. Please try again.")
            return redirect('Product_detail', pk=pk)

    return redirect('home_page')


