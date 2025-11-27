import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import JSON

# 1. Set environment to use SQLite
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# 2. Patch JSONB to work with SQLite
postgresql.JSONB = JSON

# 3. Add path to server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 4. Import app and db AFTER setting env and patching
from main import app
from database import get_db, Base
from models import User, Mentor, Car

# 5. Setup Test DB
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create initial data (User, Mentor, Car)
    db = TestingSessionLocal()
    
    # Create User
    if not db.query(User).filter_by(username="user1").first():
        user = User(username="user1", password="123456", name="Nguyễn Văn A", email="user1@example.com", isActive=True)
        db.add(user)
    
    # Create Mentor
    if not db.query(Mentor).filter_by(username="mentor1").first():
        mentor = Mentor(username="mentor1", password="123456", name="Trần Văn B", email="mentor1@example.com", isActive=True, price_per_hour=200000)
        db.add(mentor)
    
    # Create Car
    if not db.query(Car).filter_by(license_plate="30A-12345").first():
        car = Car(license_plate="30A-12345", brand="Toyota", model="Vios", status="available", price_per_hour=150000, isActive=True)
        db.add(car)
    
    db.commit()
    db.close()

@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]
