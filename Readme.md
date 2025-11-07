# Drive Coach Reservation API

API hệ thống đặt hẹn thầy dạy lái xe và xe tập lái sử dụng FastAPI và SQLAlchemy.

## Cài đặt

### Cách nhanh (Sử dụng Makefile)

> **Lưu ý:** Trên Windows, cần cài đặt Make hoặc sử dụng Git Bash/WSL để chạy các lệnh Makefile. Nếu không có Make, xem phần [Cách thủ công](#cách-thủ-công) bên dưới.

1. Cài đặt dependencies:
```bash
make install
```

2. Khởi động database và setup:
```bash
make up          # Khởi động PostgreSQL container
make reset       # Reset và tạo database schema
make master-data # Thêm dữ liệu mẫu (users, mentors, cars)
```

3. Chạy ứng dụng:
```bash
make run
```

### Cách thủ công

Nếu không sử dụng Makefile, xem chi tiết tại phần [Hướng dẫn Setup Database](#hướng-dẫn-setup-database).

## Hướng dẫn Setup Database

### Hướng dẫn nhanh (Sử dụng Makefile)

#### Setup Database đầy đủ trong 3 bước:

```bash
make up          # Khởi động PostgreSQL container
make reset       # Reset và tạo database schema (từ init.sql)
make master-data # Thêm dữ liệu mẫu (users, mentors, cars)
```

#### Các lệnh Makefile hữu ích:

```bash
make up          # Khởi động toàn bộ hệ thống (database, redis)
make down        # Dừng và xóa toàn bộ hệ thống (kèm volume)
make drop-db     # Xóa database container và volume
make reset       # Reset database: xóa bảng cũ và tạo lại schema
make master-data # Import dữ liệu mẫu vào database
make dump        # Backup database ra file db/init.sql
make logs        # Xem log các service
```

### Hướng dẫn chi tiết (Tham khảo)

#### Yêu cầu
- Docker và Docker Compose đã được cài đặt
- Make (để sử dụng Makefile) - tùy chọn nhưng khuyến nghị
- PostgreSQL client (psql) - tùy chọn, để kiểm tra database

#### Các bước setup Database (Thủ công)

#### 1. Khởi động PostgreSQL bằng Docker

Khởi động container PostgreSQL:
```bash
docker-compose up -d db
# Hoặc: make up
```

Kiểm tra container đang chạy:
```bash
docker-compose ps
```

#### 2. Kết nối vào PostgreSQL

Có thể kết nối vào database bằng một trong các cách sau:

**Cách 1: Sử dụng Docker exec**
```bash
docker-compose exec db psql -U postgres -d drive_coach
```

**Cách 2: Sử dụng psql từ máy local**
```bash
psql -h localhost -p 5432 -U postgres -d drive_coach
```
Password mặc định: `postgres`

#### 3. Tạo Database Schema

**Khuyến nghị: Sử dụng Makefile**
```bash
make reset  # Tự động reset và tạo schema từ init.sql
```

**Thủ công: Sử dụng file init.sql**

**Trên Linux/Mac:**
```bash
docker-compose exec -T db psql -U postgres -d drive_coach < db/init.sql
```

**Trên Windows PowerShell:**
```powershell
Get-Content db/init.sql | docker-compose exec -T db psql -U postgres -d drive_coach
```

**Hoặc copy file vào container rồi chạy:**
```bash
# Tìm tên container: docker-compose ps
docker cp db/init.sql <container_name>:/tmp/init.sql
docker-compose exec db psql -U postgres -d drive_coach -f /tmp/init.sql
```

**Nếu đã kết nối vào PostgreSQL:**
```sql
\i /path/to/db/init.sql
```

**Tùy chọn: Sử dụng SQLAlchemy models (Auto-create)**

Nếu ứng dụng được cấu hình để tự động tạo bảng từ models:
```bash
python -c "from models import Base; from database import engine; Base.metadata.create_all(bind=engine)"
```

#### 4. Thêm dữ liệu mẫu (Tùy chọn)

**Khuyến nghị: Sử dụng Makefile**
```bash
make master-data  # Tự động import dữ liệu mẫu
```

**Thủ công: Import dữ liệu mẫu (users, mentors, cars)**

**Trên Linux/Mac:**
```bash
docker-compose exec -T db psql -U postgres -d drive_coach < db/data-init.sql
```

**Trên Windows PowerShell:**
```powershell
Get-Content db/data-init.sql | docker-compose exec -T db psql -U postgres -d drive_coach
```

**Hoặc copy file vào container rồi chạy:**
```bash
# Tìm tên container: docker-compose ps
docker cp db/data-init.sql <container_name>:/tmp/data-init.sql
docker-compose exec db psql -U postgres -d drive_coach -f /tmp/data-init.sql
```

**Nếu đã kết nối vào PostgreSQL:**
```sql
\i /path/to/db/data-init.sql
```

#### 5. Kiểm tra Database

Kiểm tra các bảng đã được tạo:
```sql
\dt
```

Kiểm tra dữ liệu:
```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM mentors;
SELECT COUNT(*) FROM cars;
```

### Cấu hình Database Connection

Cấu hình kết nối database trong file `.env` hoặc biến môi trường:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/drive_coach
```

Hoặc thay đổi trong file `database.py` nếu cần.

### Reset Database (Nếu cần)

**Khuyến nghị: Sử dụng Makefile**
```bash
make reset       # Reset database và tạo lại schema
make master-data # Thêm lại dữ liệu mẫu (nếu cần)
```

**Hoặc xóa hoàn toàn và tạo lại:**
```bash
make drop-db     # Xóa container và volume
make up          # Khởi động lại database
make reset       # Tạo lại schema
make master-data # Thêm dữ liệu mẫu
```

**Thủ công: Sử dụng prepare.sql**

**Trên Linux/Mac:**
```bash
docker-compose exec -T db psql -U postgres -d drive_coach < db/prepare.sql
docker-compose exec -T db psql -U postgres -d drive_coach < db/init.sql
docker-compose exec -T db psql -U postgres -d drive_coach < db/data-init.sql
```

**Trên Windows PowerShell:**
```powershell
Get-Content db/prepare.sql | docker-compose exec -T db psql -U postgres -d drive_coach
Get-Content db/init.sql | docker-compose exec -T db psql -U postgres -d drive_coach
Get-Content db/data-init.sql | docker-compose exec -T db psql -U postgres -d drive_coach
```

**Xóa và tạo lại container:**
```bash
docker-compose down -v
docker-compose up -d db
# Sau đó chạy lại các bước 3 và 4
# Hoặc: make drop-db && make up && make reset && make master-data
```

### Thông tin Database

- **Host**: localhost
- **Port**: 5432
- **Database**: drive_coach
- **Username**: postgres
- **Password**: postgres
- **PostgreSQL Version**: 15

### Backup và Restore Database

**Backup database (Sử dụng Makefile):**
```bash
make dump  # Backup database ra file db/init.sql
```

**Backup database (Thủ công):**
- **Linux/Mac:** `docker-compose exec db pg_dump -U postgres drive_coach > backup.sql`
- **Windows PowerShell:** `docker-compose exec db pg_dump -U postgres drive_coach | Out-File -Encoding utf8 backup.sql`

**Restore database:**
- **Linux/Mac:** `docker-compose exec -T db psql -U postgres drive_coach < backup.sql`
- **Windows PowerShell:** `Get-Content backup.sql | docker-compose exec -T db psql -U postgres drive_coach`

### Lưu ý

- Đảm bảo port 5432 không bị chiếm dụng bởi ứng dụng khác
- Dữ liệu sẽ được lưu trong Docker volume `pgdata`
- Khuyến nghị sử dụng Makefile để đơn giản hóa các thao tác với database
- Trên Windows, cần cài đặt Git Bash hoặc WSL để chạy các script `.sh` trong Makefile
- Nếu gặp lỗi với script trên Windows, có thể chạy các lệnh thủ công như hướng dẫn ở trên

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
