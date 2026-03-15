from src.models import User
from src.app.security import get_password_hash, create_access_token


async def test_get_bikes_returns_200(client):
    response = await client.get("/bikes/")
    assert response.status_code == 200


async def test_get_bikes_returns_list(client):
    response = await client.get("/bikes/")
    data = response.json()
    assert isinstance(data, list)


async def test_create_rental_success(client, test_db_session):
    rental_data = {
        "bike_id": 1,
        "user_id": 1,
        "battery_level": 50.0,
    }
    response = await client.post("/rentals/", json=rental_data)
    assert response.status_code == 201
    body = response.json()
    assert body["bike_id"] == 1
    assert body["user_id"] == 1
    assert body["battery_level"] == 50.0


async def test_create_rental_low_battery_rejected(client, test_db_session):
    rental_data = {
        "bike_id": 1,
        "user_id": 1,
        "battery_level": 10.0,
    }
    response = await client.post("/rentals/", json=rental_data)
    assert response.status_code == 422


async def test_get_rentals_returns_200(client, test_db_session):
    response = await client.get("/rentals/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_station_requires_auth(client):
    station_data = {
        "name": "Central Station",
        "location": "Downtown",
        "capacity": 20,
    }
    response = await client.post("/stations/", json=station_data)
    assert response.status_code == 401


async def test_create_station_as_admin(client, test_db_session):
    admin_user = User(
        username="test_admin",
        is_active=True,
        hashed_password=get_password_hash("adminpass123"),
        role="admin",
    )
    test_db_session.add(admin_user)
    await test_db_session.commit()

    token = create_access_token(data={"sub": "test_admin", "role": "admin"})
    headers = {"Authorization": f"Bearer {token}"}

    station_data = {
        "name": "Central Station",
        "location": "Downtown",
        "capacity": 20,
    }
    response = await client.post(
        "/stations/", json=station_data, headers=headers
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Central Station"
    assert body["capacity"] == 20


async def test_create_station_as_rider_forbidden(client, test_db_session):
    rider_user = User(
        username="test_rider",
        is_active=True,
        hashed_password=get_password_hash("riderpass123"),
        role="rider",
    )
    test_db_session.add(rider_user)
    await test_db_session.commit()

    token = create_access_token(data={"sub": "test_rider", "role": "rider"})
    headers = {"Authorization": f"Bearer {token}"}

    station_data = {
        "name": "Rider Station",
        "location": "Suburbs",
        "capacity": 10,
    }
    response = await client.post(
        "/stations/", json=station_data, headers=headers
    )
    assert response.status_code == 403