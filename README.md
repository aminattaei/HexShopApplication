# 🛒 HexShop - Django E-commerce Web Application

![Django](https://img.shields.io/badge/Django-5.2.3-green)
![DRF](https://img.shields.io/badge/DRF-3.16.0-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)

**HexShop** is a full-featured E-commerce web application built with Django, Django REST Framework, and Bootstrap 5. It provides a complete online shopping experience including product browsing, cart management, checkout with shipping/payment, comments, and a REST API for external integrations.

The project was developed as part of a structured Django learning roadmap (sections 29–42), focusing on real-world e-commerce workflows such as authentication, cart handling, order processing, and admin dashboard management.

---

## ✨ Features

### 🛍️ Storefront
- Product catalog with category filtering (Men, Women, Kids)
- Product detail page with related products and comments
- Product listing with search
- Customer reviews on products
- Responsive design powered by Bootstrap 5
- Multilingual support: **English** + **Persian (Farsi)**

### 👤 User Authentication
- User registration and login (Django auth + custom `Customer` profile)
- Logout functionality
- Password strength validation (`zxcvbn`)
- JWT-based API authentication

### 🛒 Shopping Cart & Checkout
- Add / remove / update cart items
- Cart summary with tax and flat-rate shipping calculation
- Shipping address form
- Order creation from cart items
- Payment confirmation / cancellation flow
- Automatic cart clearing after successful order
- Global cart item count via context processor

### 📦 Admin Panel (Django Admin)
- Manage products, categories, and customers
- Order management with inline `OrderItem` editing
- Cart management with inline `CartItem` editing
- Comment moderation
- Contact message inbox
- Search, filter, and inline editing for all registered models

### 🔌 REST API
- Product CRUD API endpoint (`/api/products/`)
- JWT token obtain, refresh, and verify endpoints
- Interactive API documentation with **Swagger UI** and **ReDoc**
- OpenAPI schema endpoint

### 🌍 Internationalization
- Persian (Farsi) + English language support
- Locale-aware URL routing (`django-modeltranslation`)
- Model field translations

---

## 🛠 Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| **Django** | 5.2.3 | Web framework |
| **Django REST Framework** | 3.16.0 | REST API |
| **SimpleJWT** | 5.5.0 | JWT authentication |
| **drf-spectacular** | 0.28.0 | API schema & docs |
| **crispy-bootstrap5** | 2025.6 | Form rendering |
| **django-modeltranslation** | 0.19.16 | i18n |
| **PostgreSQL** | — | Database (production) |
| **Bootstrap 5** | — | Front-end CSS framework |
| **Pillow** | 11.2.1 | Image upload handling |

---

## 📁 Project Structure

```
HexShopApplication/
├── ShopConfig/                  # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── store/                       # Main Django app
│   ├── models.py                # Category, Customer, Product, Order, OrderItem, Cart, CartItem, Comment, Contact, ShippingAddress
│   ├── views.py                 # Storefront, auth, cart, shipping, payment, and API views
│   ├── urls.py                  # App-level URL routing + API + schema endpoints
│   ├── serializers.py           # DRF serializers (Product, Category)
│   ├── forms.py                 # ContactForm, CommentForm, ShippingAddressForm
│   ├── admin.py                 # Django Admin config with inlines
│   ├── signals.py               # pre_save signal for auto-setting shipped_date
│   ├── context_processors.py    # cart_items_count global context
│   ├── translation.py           # Translation strings
│   ├── tests.py                 # Unit tests
│   └── migrations/              # Database migrations
├── templates/                   # HTML templates
│   ├── base.html
│   ├── Index/                   # Home, about, contact, products, category, single-product
│   ├── cart/                    # cart_summary, shipping, payment
│   ├── registration/            # login, signup
│   └── partials/                # header, footer
├── static/                      # CSS, JS, images, fonts
├── locale/                      # Translation files (if generated)
├── Docs/                        # Project notes and learning roadmap
│   ├── details.txt              # Detailed view descriptions
│   └── notes.txt                # Learning roadmap (sections 29–42)
├── convert_static.py            # Utility script to convert raw static links to Django {% static %} tags
├── requirements.txt             # Python dependencies
├── manage.py
└── README.md
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- PostgreSQL 12+ (or SQLite for quick local testing)
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/HexShopApplication.git
cd HexShopApplication

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure database
# For production, update ShopConfig/settings.py with your PostgreSQL credentials.
# For quick local testing, switch to SQLite:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# 5. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 6. (Optional) Create superuser for Django Admin
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

Open your browser:
- **Storefront:** [http://127.0.0.1:8000/store/](http://127.0.0.1:8000/store/)
- **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **API Docs (Swagger):** [http://127.0.0.1:8000/store/api/schema/swagger-ui/](http://127.0.0.1:8000/store/api/schema/swagger-ui/)
- **API Docs (ReDoc):** [http://127.0.0.1:8000/store/api/schema/redoc/](http://127.0.0.1:8000/store/api/schema/redoc/)

---

## ⚙️ Configuration

### Database
The project uses **PostgreSQL** by default. To use SQLite locally, update `DATABASES` in `ShopConfig/settings.py`.

### Secret Key
⚠️ **Never commit your real `SECRET_KEY` to version control.** Generate a secure key and store it as an environment variable:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Set it in production via environment variables or a `.env` file using `python-dotenv`.

### Media Files
Product images and user uploads are stored in `/media/`. Ensure your web server serves this directory in production.

### Environment Variables (Recommended for Production)
For production deployments, use `python-dotenv` or `django-environ` to manage:

- `SECRET_KEY`
- `DEBUG` (set to `False`)
- `DATABASE_URL`
- `ALLOWED_HOSTS`

---

## 🔑 API Usage

### Authentication
All API endpoints require JWT authentication by default.

```bash
# Obtain token
curl -X POST http://127.0.0.1:8000/store/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'

# Use token
curl http://127.0.0.1:8000/store/api/products/ \
  -H "Authorization: Bearer <your_token>"
```

### Available Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/store/api/products/` | List all products (requires auth) |
| `POST` | `/store/api/products/` | Create a product (requires auth) |
| `GET` | `/store/api/products/{id}/` | Retrieve a product (requires auth) |
| `PUT` | `/store/api/products/{id}/` | Update a product (requires auth) |
| `DELETE` | `/store/api/products/{id}/` | Delete a product (requires auth) |
| `POST` | `/store/api/token/` | Obtain JWT token pair |
| `POST` | `/store/api/token/refresh/` | Refresh JWT token |
| `POST` | `/store/api/token/verify/` | Verify JWT token |

> **Note:** The product listing API requires authentication by default. This is intentional for this project but can be relaxed by updating `REST_FRAMEWORK` permissions in `settings.py`.

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 🗺️ Roadmap & Known Issues

- [x] Product CRUD and listing
- [x] Cart and checkout flow
- [x] JWT authentication
- [x] API with Swagger/ReDoc docs
- [x] Persian + English i18n
- [x] Admin inlines for orders and carts
- [x] Auto-set shipped_date signal
- [ ] Shipping dashboard for admins (section 39)
- [ ] Dashboard item detail pages (section 40)
- [ ] Shipped status buttons in admin (section 41)
- [ ] Coupon/discount code system
- [ ] Multi-image upload for products
- [ ] Password reset flow
- [ ] Production deployment guide

### Known Code Issues
- `SPECTACULAR_SETTINGS` is defined twice in `ShopConfig/settings.py`. The second definition overwrites the first. Consolidate into a single dictionary.
- `SECRET_KEY` and database credentials are hardcoded in `settings.py`. Move to environment variables for production.
- The `Customer` model duplicates fields from Django's built-in `User` model. Consider migrating to a `OneToOneField` profile for production.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- This project was built following a structured Django e-commerce learning roadmap.
- Design inspired by the **HexaShop** Bootstrap template.
- Thanks to the Django and DRF communities for excellent documentation.
