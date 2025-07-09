from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from datetime import datetime


class Category(models.Model):
    name = models.CharField(_("category name"), max_length=50)

    description = models.TextField(default="", blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})


class Customer(models.Model):
    first_name = models.CharField(_("first_name"), max_length=50)

    last_name = models.CharField(_("last_name"), max_length=50)

    phone = models.CharField(_("phone number"), max_length=11)

    email = models.EmailField(_("email"), max_length=254)

    password = models.CharField(_("password"), max_length=50)

    class Meta:
        verbose_name = _("customer")
        verbose_name_plural = _("customers")

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    name = models.CharField(_("product name"), max_length=50)

    price = models.DecimalField(
        _("product price "), max_digits=6, decimal_places=2, default=0
    )

    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    description = models.TextField(_("product  description"))

    image = models.ImageField(_("product image"), upload_to="uploads/product/")

    is_sale = models.BooleanField(default=False)

    sale_price = models.DecimalField(
        _("product price "), max_digits=6, decimal_places=2, default=0, blank=True
    )

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=11, blank=True)
    date = models.DateField(default=datetime.today)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f"Order #{self.id} by {self.customer.first_name}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.product.price * self.quantity



class Contact(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message = models.TextField()

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse("Contact_detail", kwargs={"pk": self.pk})


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"Cart #{self.id} - Customer: {self.customer.first_name}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.product.price * self.quantity


class Comment(models.Model):
    product = models.ForeignKey(
        Product, verbose_name=_("product"), on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        Customer, verbose_name=_("customer"), on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"Comment by {self.customer} on {self.product}"


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.IntegerField()
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("ShippingAddress")
        verbose_name_plural = _("ShippingAddresses")

    def __str__(self):
        return f"{self.address}, {self.city}"
