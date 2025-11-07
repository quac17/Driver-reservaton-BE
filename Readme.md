# Drive Coach Reservation API

API hệ thống đặt hẹn thầy dạy lái xe và xe tập lái sử dụng FastAPI và SQLAlchemy.

## Cài đặt

1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

2. Khởi động database:
```bash
docker-compose up -d db
```

3. Chạy ứng dụng:
```bash
python main.py
```

Hoặc sử dụng uvicorn:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Authentication

#### Đăng nhập (Login)
```
POST /authen/login
Content-Type: application/x-www-form-urlencoded

username=user1&password=123456
```
**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "message": {
    "loginData": {
      "username": "user1",
      "name": "Nguyễn Văn A",
      "isMentor": false,
      "email": "user1@example.com",
      "phone": "0901234567"
    }
  }
}
```

#### Đăng xuất (Logout)
```
POST /authen/logout
Authorization: Bearer <access_token>
```

#### Làm mới token (Reset token)
```
POST /authen/reset-token
Authorization: Bearer <access_token>
```

### Users

#### Lấy tất cả users
```
GET /user/
Authorization: Bearer <access_token>
```

#### Lấy user theo ID
```
GET /user/{user_id}
Authorization: Bearer <access_token>
```

#### Tạo user mới
```
POST /user/
Content-Type: application/json

{
  "username": "user1",
  "name": "Nguyễn Văn A",
  "password": "123456",
  "email": "user1@example.com",
  "phone": "0901234567",
  "address": "123 Đường ABC, Quận 1, TP.HCM"
}
```

#### Cập nhật user
```
PUT /user/{user_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Nguyễn Văn A Updated",
  "email": "newemail@example.com",
  "phone": "0901234568"
}
```

#### Xóa user (soft delete)
```
DELETE /user/{user_id}
Authorization: Bearer <access_token>
```

### Mentors

#### Lấy danh sách mentors
```
GET /mentor/
```

#### Lấy mentor theo ID
```
GET /mentor/{mentor_id}
```

### Cars

#### Lấy danh sách cars
```
GET /car/
GET /car/?status=available
```

#### Lấy car theo ID
```
GET /car/{car_id}
```

### Reserves (Đặt lịch hẹn)

#### Lấy danh sách reserves
```
GET /reserve/
GET /reserve/?status=pending
GET /reserve/?user_id=1
GET /reserve/?mentor_id=1
Authorization: Bearer <access_token>
```
- User chỉ xem được reserves của chính mình
- Mentor chỉ xem được reserves của chính mình

#### Lấy reserve theo ID
```
GET /reserve/{reserve_id}
Authorization: Bearer <access_token>
```

#### Đặt lịch hẹn
```
POST /reserve/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user_id": 1,
  "mentor_id": 1,
  "car_id": 1,
  "status": "pending",
  "reserve_details": [
    {
      "start_time": "2025-01-25T08:00:00+00:00",
      "end_time": "2025-01-25T10:00:00+00:00",
      "price": 500000,
      "notes": "Học buổi sáng",
      "status": "pending"
    },
    {
      "start_time": "2025-01-26T14:00:00+00:00",
      "end_time": "2025-01-26T16:00:00+00:00",
      "price": 500000,
      "notes": "Học buổi chiều",
      "status": "pending"
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "mentor_id": 1,
  "car_id": 1,
  "status": "pending",
  "createdAt": "2025-01-25T07:00:00+00:00",
  "updatedAt": "2025-01-25T07:00:00+00:00",
  "reserve_details": [
    {
      "id": 1,
      "reserve_id": 1,
      "start_time": "2025-01-25T08:00:00+00:00",
      "end_time": "2025-01-25T10:00:00+00:00",
      "price": 500000,
      "notes": "Học buổi sáng",
      "status": "pending",
      "createdAt": "2025-01-25T07:00:00+00:00",
      "updatedAt": "2025-01-25T07:00:00+00:00"
    }
  ]
}
```

## Cấu trúc Project

```
DriveCoachReservation/
├── main.py              # FastAPI app chính
├── database.py          # Cấu hình database connection
├── models.py            # SQLAlchemy models (User, Mentor, Car, Reserve, ReserveDetail)
├── schemas.py           # Pydantic schemas cho API
├── routers/             # API routers
│   ├── __init__.py
│   ├── authen.py        # Authentication endpoints
│   ├── user.py          # User API endpoints
│   ├── mentor.py        # Mentor API endpoints
│   ├── car.py           # Car API endpoints
│   └── reserve.py       # Reserve API endpoints
├── requirements.txt     # Dependencies
├── docker-compose.yml   # Docker setup
├── Dockerfile          # Docker image
├── Makefile            # Lệnh tiện ích
├── db/                 # Database scripts
│   ├── init.sql        # Database schema
│   ├── prepare.sql     # Drop tables script
│   └── data-init.sql   # Initial data
└── scripts/            # Utility scripts
```

## Database Schema

### Users
- Khách hàng đặt hẹn
- Fields: id, username, password, name, email, phone, address, isActive, createdAt, updatedAt

### Mentors
- Thầy dạy lái xe
- Fields: id, username, password, name, email, phone, license_number, experience_years, isActive, createdAt, updatedAt

### Cars
- Xe tập lái
- Fields: id, license_plate, brand, model, color, year, status, isActive, createdAt, updatedAt
- Status: available, busy, maintenance

### Reserves
- Đặt hẹn
- Fields: id, user_id, mentor_id, car_id, status, createdAt, updatedAt
- Status: pending, confirmed, cancelled, completed

### Reserve Details
- Chi tiết đặt hẹn (thời gian cụ thể)
- Fields: id, reserve_id, start_time, end_time, price, notes, status, createdAt, updatedAt
- Status: pending, confirmed, cancelled, completed

## Tính năng

- ✅ REST API với FastAPI
- ✅ Authentication với JWT (hỗ trợ User và Mentor)
- ✅ CRUD operations cho User
- ✅ GET operations cho Mentor, Car, Reserve
- ✅ Đặt lịch hẹn với kiểm tra xung đột thời gian
- ✅ Validation với Pydantic
- ✅ Database với SQLAlchemy + PostgreSQL
- ✅ Error handling
- ✅ Auto-generated API docs tại `/docs`
- ✅ Phân quyền: User chỉ xem reserves của chính mình
- ✅ Timestamp fields (createdAt, updatedAt)

## Truy cập API Documentation

Sau khi chạy server, truy cập:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Lưu ý

- Tất cả API cần authentication (trừ POST /user/ và GET /mentor/, GET /car/)
- Chỉ User mới có thể đặt lịch hẹn
- Hệ thống tự động kiểm tra xung đột thời gian khi đặt lịch
- Car phải có status = "available" mới có thể đặt lịch
