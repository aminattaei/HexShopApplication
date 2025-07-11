# Generated by Django 5.2.3 on 2025-06-20 05:07

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="نام دسته بندی")),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", verbose_name="توضیحات دسته بندی"
                    ),
                ),
            ],
            options={
                "verbose_name": "دسته بندی",
                "verbose_name_plural": "دسته بندی ها",
            },
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50, verbose_name="نام")),
                (
                    "last_name",
                    models.CharField(max_length=50, verbose_name="نام خانوادگی"),
                ),
                ("phone", models.CharField(max_length=11, verbose_name="شماره تماس")),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="پست الکترونیکی"),
                ),
                ("password", models.CharField(max_length=50, verbose_name="رمز عبور")),
            ],
            options={
                "verbose_name": "دسته بندی",
                "verbose_name_plural": "دسته بندی ها",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="نام محصول")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=3,
                        default=0,
                        max_digits=9,
                        verbose_name="قیمت محصول",
                    ),
                ),
                ("description", models.TextField(verbose_name="توضیحات محصول")),
                (
                    "image",
                    models.ImageField(
                        upload_to="uploads/product/", verbose_name="تصویر محصول"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.category",
                        verbose_name="products",
                    ),
                ),
            ],
            options={
                "verbose_name": "دسته بندی",
                "verbose_name_plural": "دسته بندی ها",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(verbose_name="تعداد محصول")),
                ("address", models.TextField(verbose_name="آدرس")),
                ("phone", models.CharField(blank=True, verbose_name="شماره تماس")),
                (
                    "date",
                    models.DateField(
                        default=datetime.datetime.today, verbose_name="زمان"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(default=False, verbose_name="ضعیت سفارش"),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.customer"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.product"
                    ),
                ),
            ],
            options={
                "verbose_name": "سفارش",
                "verbose_name_plural": "سفارشات",
            },
        ),
    ]
