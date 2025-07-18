# 🛒 Django E-commerce Web Application

This is a full-featured E-commerce web application built with Django and Django Rest Framework. It supports user authentication, product management, cart handling, and order processing.

## Features

- JWT-based authentication system
- Role-based access control (admin/customer)
- User profile management (with avatar upload)
- Product/category CRUD operations
- Shopping cart and order tracking
- Contact form with DB storage
- Admin panel using Django Admin

## Tech Stack

- Django 4.x
- Django Rest Framework
- JWT Authentication
- SQLite (development) – PostgreSQL recommended for production
- Front-end based on HTML/CSS and Bootstrap

## Installation

```bash
git clone https://github.com/yourusername/ecommerce-app.git
cd ecommerce-app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
