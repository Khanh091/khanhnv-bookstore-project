# Microservices Architecture - Bookstore

Hệ thống Bookstore được chia thành 3 microservices độc lập:

1. **customer-service** (Port 8001): Quản lý customer registration và login
2. **book-service** (Port 8002): Quản lý book catalog
3. **cart-service** (Port 8003): Quản lý shopping cart

## Cấu trúc

```
micro/
├── customer-service/     # Customer service + API Gateway
│   ├── customers/        # Customer model & API
│   └── gateway/          # Frontend/Gateway (tích hợp tất cả services)
├── book-service/         # Book service
│   └── books/            # Book model & API
└── cart-service/         # Cart service
    └── carts/            # Cart & CartItem models & API
```

## Database

Mỗi service sử dụng MySQL database riêng:
- `customer_service_db` - cho customer-service
- `book_service_db` - cho book-service
- `cart_service_db` - cho cart-service

## Cài đặt và Chạy

### 1. Cài đặt dependencies

```bash
pip install django requests mysqlclient
```

### 2. Migrations

```bash
# Customer service
cd micro/customer-service
python manage.py makemigrations
python manage.py migrate

# Book service
cd micro/book-service
python manage.py makemigrations
python manage.py migrate

# Cart service
cd micro/cart-service
python manage.py makemigrations
python manage.py migrate
```

### 3. Chạy các services

Mở 3 terminal windows:

**Terminal 1 - Customer Service (Port 8001):**
```bash
cd micro/customer-service
python manage.py runserver 8001
```

**Terminal 2 - Book Service (Port 8002):**
```bash
cd micro/book-service
python manage.py runserver 8002
```

**Terminal 3 - Cart Service (Port 8003):**
```bash
cd micro/cart-service
python manage.py runserver 8003
```

### 4. Truy cập

- **Frontend/Gateway**: http://127.0.0.1:8001/
- **Customer API**: http://127.0.0.1:8001/api/customers/
- **Book API**: http://127.0.0.1:8002/api/books/
- **Cart API**: http://127.0.0.1:8003/api/carts/

## API Endpoints

### Customer Service (8001)

- `POST /api/customers/register/` - Register customer
- `POST /api/customers/login/` - Login customer
- `GET /api/customers/<id>/` - Get customer by ID

### Book Service (8002)

- `GET /api/books/` - List all books
- `GET /api/books/<id>/` - Get book by ID

### Cart Service (8003)

- `POST /api/carts/add/` - Add book to cart
- `GET /api/carts/<customer_id>/` - Get cart contents

## Frontend (Gateway)

Gateway được tích hợp trong customer-service, cung cấp:
- `/register/` - Registration page
- `/login/` - Login page
- `/catalog/` - Book catalog page
- `/cart/` - Shopping cart page

Gateway tự động gọi các microservices APIs để lấy và hiển thị dữ liệu.
