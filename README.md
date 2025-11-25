# 🏷️ JerseyShop

**JerseyShop** is a specialized e-commerce platform built with Django and Django REST Framework (DRF), dedicated exclusively to selling sports jerseys. It features secure JWT authentication, full product and order management, a payment gateway powered by SSLCommerz, and auto-generated API documentation.

---

## 🚀 Features

- ✅ User registration, login, and profile management (JWT auth via Djoser)
- 👕 Jersey product listing with details
- 🛒 Order creation and tracking
- 💳 Payment gateway integration with **SSLCommerz**
- 🔐 JWT-based authentication
- 📄 Auto-generated API docs (Swagger & Redoc via drf-yasg)
- 🛠️ Admin dashboard for staff
- 📦 RESTful API architecture

---

## ⚙️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Authentication:** Djoser + JWT
- **Payment Gateway:** [SSLCommerz](https://sslcommerz.com/)
- **API Documentation:** drf-yasg
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Hosting:** (Add your hosting info here, e.g., Render, Railway, Heroku)

---
## 🔐 Authentication

Implemented with **Djoser** and **JWT**:

| Endpoint                  | Purpose                     |
|--------------------------|-----------------------------|
| `/auth/jwt/create/`      | Get access & refresh tokens |
| `/auth/jwt/refresh/`     | Refresh access token        |
| `/auth/users/`           | Register new users          |
| `/auth/users/me/`        | Get current user info       |

---

## 💳 Payment Integration

The site uses **SSLCommerz** to handle secure payments.

| Endpoint                        | Purpose                             |
|----------------------------------|-------------------------------------|
| `/api/orders/initiate/`     | Start payment session with gateway |
| `/api/orders/success/`      | Callback for successful payment    |
| `/api/orders/fail/`         | Callback for failed payment        |
| `/api/orders/cancel/`       | Callback for canceled payment      |

> ✅ Ensure that your `settings.py` includes valid `SSLCommerz` store credentials and URLs.

---

## 📄 API Documentation

Swagger and Redoc auto-generated API docs available at:

- **Swagger UI:** `*/swagger/`  
- **Redoc UI:** `*/redoc/`  

Powered by **drf-yasg**.

---
## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (or your database of choice)
- pip

## 🧪 Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/jerseyshop.git
   cd jerseyshop
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   #On Linux use source venv/bin/activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Apply migrations:
   ```bash
   python manage.py migrate
5. Run server:
   ```bash
   python manage.py runserver
## 📝 Environment Variables
Create a .env file in the root and add the following (example):

    SECRET_KEY=your-secret-key
    DEBUG=True
    DATABASE_URL=your-db-url
    ALLOWED_HOSTS=127.0.0.1,localhost
---
## 📄 License
This project is licensed under the MIT License.

## ✉️ Contact
Email: parthokumarmondal90@gmail.com


<div align="right"> 
    developed by Partho
</div>

