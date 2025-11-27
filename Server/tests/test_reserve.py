import pytest
from datetime import datetime, timedelta
from database import get_db
from models import Car

# Test Data
USER_CREDENTIALS = {"username": "user1", "password": "123456"}
MENTOR_CREDENTIALS = {"username": "mentor1", "password": "123456"}
USER_ID = 1
MENTOR_ID = 1
CAR_ID = 1

def get_auth_token(client, credentials):
    response = client.post("/authen/login", data=credentials)
    assert response.status_code == 200
    return response.json()["access_token"]

def test_search_available_cars(client):
    """RESERVE-01: Search for available mentors/cars within a specific time slot."""
    # Note: API currently only supports status filter
    response = client.get("/car/?status=available")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_reserve_success(client):
    """RESERVE-04: Successful booking with valid data (Available Mentor and Car)"""
    token = get_auth_token(client, USER_CREDENTIALS)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Use a time far in the future to avoid conflicts with previous runs
    start_time = datetime.now() + timedelta(days=365)
    end_time = start_time + timedelta(hours=2)
    
    payload = {
        "user_id": USER_ID,
        "mentor_id": MENTOR_ID,
        "car_id": CAR_ID,
        "reserve_details": [
            {
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "notes": "Test booking success"
            }
        ]
    }
    
    response = client.post("/reserve/", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert len(data["reserve_details"]) == 1

def test_create_reserve_conflict(client):
    """RESERVE-02/03/06: Failed booking because the car is already reserved"""
    token = get_auth_token(client, USER_CREDENTIALS)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a booking first
    start_time = datetime.now() + timedelta(days=366)
    end_time = start_time + timedelta(hours=2)
    
    payload = {
        "user_id": USER_ID,
        "mentor_id": MENTOR_ID,
        "car_id": CAR_ID,
        "reserve_details": [
            {
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "notes": "First booking"
            }
        ]
    }
    client.post("/reserve/", json=payload, headers=headers)
    
    # Try to book exact same slot
    response = client.post("/reserve/", json=payload, headers=headers)
    assert response.status_code == 400
    assert "Xe đã được đặt" in response.json()["detail"]
    
    # Try to book overlapping slot (RESERVE-03)
    payload_overlap = payload.copy()
    payload_overlap["reserve_details"] = [{
        "start_time": (start_time + timedelta(hours=1)).isoformat(),
        "end_time": (end_time + timedelta(hours=1)).isoformat()
    }]
    response = client.post("/reserve/", json=payload_overlap, headers=headers)
    assert response.status_code == 400
    assert "Xe đã được đặt" in response.json()["detail"]

def test_create_reserve_mentor_conflict(client, db):
    """RESERVE-05: Failed booking because the mentor is already reserved"""
    # Need a second car to test mentor conflict specifically (same mentor, different car)
    # Since we can't create car via API, we use DB session directly
    try:
        # Create temp car
        temp_car = Car(
            license_plate=f"TEMP-{datetime.now().timestamp()}",
            brand="Test",
            model="Car",
            status="available",
            price_per_hour=50,
            isActive=True
        )
        db.add(temp_car)
        db.commit()
        db.refresh(temp_car)
        
        token = get_auth_token(client, USER_CREDENTIALS)
        headers = {"Authorization": f"Bearer {token}"}
        
        start_time = datetime.now() + timedelta(days=367)
        end_time = start_time + timedelta(hours=2)
        
        # Booking 1: Mentor + Original Car
        payload1 = {
            "user_id": USER_ID,
            "mentor_id": MENTOR_ID,
            "car_id": CAR_ID,
            "reserve_details": [
                {
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat()
                }
            ]
        }
        client.post("/reserve/", json=payload1, headers=headers)
        
        # Booking 2: Mentor + Temp Car
        payload2 = {
            "user_id": USER_ID,
            "mentor_id": MENTOR_ID,
            "car_id": temp_car.id,
            "reserve_details": [
                {
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat()
                }
            ]
        }
        response = client.post("/reserve/", json=payload2, headers=headers)
        
        # Check for failure (Mentor conflict)
        # Note: If system doesn't check mentor conflict, this will be 201.
        # We assert 400 as per requirement.
        assert response.status_code == 400
        assert "Mentor đã được đặt" in response.json()["detail"]
        
    finally:
        # Cleanup temp car
        if 'temp_car' in locals():
            db.delete(temp_car)
            db.commit()
        db.close()

def test_create_reserve_inactive_entity(client, db):
    """RESERVE-07: Failed booking because the mentor or car is in an inactive state"""
    # Create inactive car via DB
    try:
        inactive_car = Car(
            license_plate=f"INACTIVE-{datetime.now().timestamp()}",
            status="available",
            isActive=False
        )
        db.add(inactive_car)
        db.commit()
        db.refresh(inactive_car)
        
        token = get_auth_token(client, USER_CREDENTIALS)
        headers = {"Authorization": f"Bearer {token}"}
        
        payload = {
            "user_id": USER_ID,
            "mentor_id": MENTOR_ID,
            "car_id": inactive_car.id,
            "reserve_details": [
                {
                    "start_time": (datetime.now() + timedelta(days=368)).isoformat(),
                    "end_time": (datetime.now() + timedelta(days=368, hours=1)).isoformat()
                }
            ]
        }
        
        response = client.post("/reserve/", json=payload, headers=headers)
        assert response.status_code == 404
        assert "Car không tồn tại" in response.json()["detail"]
        
    finally:
        if 'inactive_car' in locals():
            db.delete(inactive_car)
            db.commit()
        db.close()
