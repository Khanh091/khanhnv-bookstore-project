# Frontend - Bookstore

Frontend riêng biệt sử dụng HTML, CSS, JavaScript thuần (vanilla JS) không phụ thuộc Django.

## Cấu trúc

```
frontend/
├── index.html      # Trang login/register
├── catalog.html    # Trang catalog sách
├── cart.html       # Trang shopping cart
├── config.js       # Cấu hình API endpoints
├── app.js          # Utility functions và authentication
├── catalog.js      # Logic cho trang catalog
├── cart.js         # Logic cho trang cart
└── styles.css      # Styles CSS
```

## Cách sử dụng

1. **Mở file index.html** trong trình duyệt (hoặc dùng local server):
   ```bash
   # Cách 1: Mở trực tiếp file
   # Click đúp vào index.html

   # Cách 2: Dùng Python HTTP server
   cd micro/frontend
   python -m http.server 8080
   # Sau đó truy cập http://localhost:8080
   ```

2. **Đảm bảo các microservices đang chạy:**
   - Customer Service (8001)
   - Book Service (8002)
   - Cart Service (8003)

## Tính năng

- ✅ **Authentication**: Login/Register với Customer Service
- ✅ **Book Catalog**: Hiển thị danh sách sách từ Book Service
- ✅ **Add to Cart**: Thêm sách vào giỏ hàng qua Cart Service
- ✅ **View Cart**: Xem giỏ hàng với thông tin chi tiết sách

## Lợi ích

- **No Backend Dependency**: Không cần Django server cho frontend
- **Simple**: Chỉ cần HTML/CSS/JS thuần
- **Fast**: Không có server-side rendering overhead
- **Portable**: Có thể deploy bất kỳ đâu (static hosting)

## Lưu ý

- Sử dụng `localStorage` để lưu customer ID và name
- CORS có thể cần được cấu hình trên các services nếu deploy trên domains khác nhau
- Đối với production, nên sử dụng HTTPS
