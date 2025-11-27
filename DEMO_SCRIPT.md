

## 1. Files Kỹ Thuật (Agile Demo)

### 📂 Backend (FastAPI)
- **`Server/main.py`** - Entry point, cấu hình API
- **`Server/models.py`** - Database models (User, Mentor, Car, Reserve)
- **`Server/schemas.py`** - Pydantic schemas cho validation
- **`Server/database.py`** - Database connection setup
- **`Server/routers/`** - API endpoints:
  - `auth.py` - Authentication (login, register)
  - `reserve.py` - Reservation CRUD operations
  - `mentor.py` - Mentor management
  - `car.py` - Car management
- **`Server/tests/`** - Unit tests:
  - `conftest.py` - Test fixtures và setup
  - `test_auth.py` - Authentication tests
  - `test_reserve.py` - Reservation logic tests

### 📂 Frontend (Next.js)
- **`Client/app/login/page.tsx`** - Login page
- **`Client/app/dashboard/page.tsx`** - Dashboard overview
- **`Client/app/reserve/page.tsx`** - Reservation list
- **`Client/app/reserve/new/page.tsx`** - Create new reservation
- **`Client/app/reserve/[id]/page.tsx`** - Reservation detail
- **`Client/lib/api.ts`** - API client functions

### 📂 DevOps & Config
- **`Server/Makefile`** - Development commands
- **`Server/docker-compose.yml`** - PostgreSQL setup
- **`Server/requirements.txt`** - Python dependencies
- **`Client/package.json`** - Node.js dependencies

### 📂 Documentation
- **`README.md`** - Project overview và setup instructions
- **`Server/Readme.md`** - API documentation chi tiết
- **`DEMO_SCRIPT.md`** - File này (hướng dẫn demo)

---

## 2. Agile Artifacts (Tùy chọn show)
- **Testing**: Coverage report từ pytest (`Server/tests/`)
- **Documentation**: API docs tự động tại `/docs` (FastAPI Swagger)
