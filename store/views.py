from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm


from .models import Product


def Home_Page(request):
    return render(request, "Index/index.html", {})


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

    context = {"product": product}

    return render(request, "Index/single-product.html", context)


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Your account was successfully created!")
            login(request, user)
            return redirect("home_page")
        else:
            messages.error(
                request,
                "The username or password is incorrect. Please try again or contact the support team.",
            )
            return redirect("register")

    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


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
            print(messages.success)
            return redirect("home_page")
        else:
            messages.error(
                request,
                "Username or Password is Wrong! Please Retype username and password or Try Again Later.",
            )
            return redirect("login")
    else:
        return render(request, "registration/login.html", {})
