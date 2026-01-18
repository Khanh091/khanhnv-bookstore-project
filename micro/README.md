# Microservices Architecture - Bookstore

Hệ thống Bookstore được chia thành 3 microservices độc lập:

1. **customer-service** (Port 8001): Quản lý customer registration và login
2. **book-service** (Port 8002): Quản lý book catalog
3. **cart-service** (Port 8003): Quản lý shopping cart

## Cấu trúc

```
micro/
├── frontend/             # Frontend riêng biệt (HTML/CSS/JS thuần)
│   ├── index.html       # Login/Register page
│   ├── catalog.html     # Book catalog page
│   ├── cart.html        # Shopping cart page
│   └── *.js, *.css     # JavaScript & CSS files
├── customer-service/     # Customer service
│   └── customers/        # Customer model & API
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

**Frontend:**
- Mở file `micro/frontend/index.html` trong trình duyệt
- Hoặc chạy: `cd micro/frontend && python -m http.server 8080`
- Truy cập: http://localhost:8080

**API Endpoints:**
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

## Frontend

Frontend sử dụng HTML/CSS/JavaScript thuần, không phụ thuộc Django:
- `index.html` - Login/Register page
- `catalog.html` - Book catalog page
- `cart.html` - Shopping cart page

**Lợi ích:**
- ✅ Không cần Django server cho frontend
- ✅ Đơn giản, nhanh, dễ deploy
- ✅ Có thể host bất kỳ đâu (static hosting)
- ✅ Không có server-side rendering overhead
- ✅ Không cần migrations hay database

**Cách sử dụng:**
```bash
cd micro/frontend
python -m http.server 8080
# Hoặc chỉ cần mở index.html trong trình duyệt
```
