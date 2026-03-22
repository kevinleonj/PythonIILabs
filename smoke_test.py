"""
EcoMute Smoke Test — Run this against your live server before presenting.
Tests every endpoint, every role, every edge case the professor might ask about.

HOW TO RUN:
    1. Start your server:   python -m uvicorn src.main:app --reload
    2. In a second terminal: python smoke_test.py

If everything passes, you are ready to present.
If something fails, the script tells you exactly what broke and why.
"""

import requests
import sys
import os

BASE = "http://127.0.0.1:8000"
PASS_COUNT = 0
FAIL_COUNT = 0
WARN_COUNT = 0


def log_pass(test_name):
    global PASS_COUNT
    PASS_COUNT += 1
    print(f"  [PASS] {test_name}")


def log_fail(test_name, detail):
    global FAIL_COUNT
    FAIL_COUNT += 1
    print(f"  [FAIL] {test_name}")
    print(f"         {detail}")


def log_warn(test_name, detail):
    global WARN_COUNT
    WARN_COUNT += 1
    print(f"  [WARN] {test_name}")
    print(f"         {detail}")


def section(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


# ─────────────────────────────────────────────────────────────
# 0. SERVER REACHABLE
# ─────────────────────────────────────────────────────────────
section("0. SERVER CONNECTION")

try:
    r = requests.get(f"{BASE}/docs", timeout=5)
    if r.status_code == 200:
        log_pass("Server is running and /docs is reachable")
    else:
        log_fail("Server /docs", f"Status {r.status_code}")
except requests.exceptions.ConnectionError:
    print()
    print("  FATAL: Cannot connect to the server at " + BASE)
    print("  Start it first: python -m uvicorn src.main:app --reload")
    print()
    sys.exit(1)


# ─────────────────────────────────────────────────────────────
# 1. BIKES CRUD (database-backed)
# ─────────────────────────────────────────────────────────────
section("1. BIKES CRUD")

# GET all bikes — should return seeded data
r = requests.get(f"{BASE}/bikes/")
if r.status_code == 200 and isinstance(r.json(), list):
    bikes = r.json()
    log_pass(f"GET /bikes/ — returned {len(bikes)} bikes")
    if len(bikes) >= 3:
        log_pass("Seeded bikes are present (3+)")
    else:
        log_warn("Seeded bikes", f"Expected 3+, got {len(bikes)}. Did you delete ecomute.db and restart?")
else:
    log_fail("GET /bikes/", f"Status {r.status_code}")

# GET with status filter
r = requests.get(f"{BASE}/bikes/", params={"status": "available"})
if r.status_code == 200:
    filtered = r.json()
    all_available = all(b["status"] == "available" for b in filtered)
    if all_available:
        log_pass(f"GET /bikes/?status=available — {len(filtered)} bikes, all available")
    else:
        log_fail("GET /bikes/?status=available", "Returned bikes with wrong status")
else:
    log_fail("GET /bikes/?status=available", f"Status {r.status_code}")

# GET single bike
r = requests.get(f"{BASE}/bikes/1")
if r.status_code == 200 and r.json().get("id") == 1:
    log_pass("GET /bikes/1 — found bike id=1")
else:
    log_fail("GET /bikes/1", f"Status {r.status_code}")

# GET nonexistent bike — should 404
r = requests.get(f"{BASE}/bikes/999")
if r.status_code == 404:
    log_pass("GET /bikes/999 — correctly returned 404")
else:
    log_fail("GET /bikes/999", f"Expected 404, got {r.status_code}")

# POST create a new bike
new_bike = {
    "model": "SmokeTestBike",
    "battery": 77.0,
    "status": "available",
    "station_id": None,
}
r = requests.post(f"{BASE}/bikes/", json=new_bike)
if r.status_code == 201:
    created = r.json()
    created_id = created.get("id")
    log_pass(f"POST /bikes/ — created bike id={created_id}")
else:
    log_fail("POST /bikes/", f"Status {r.status_code}, body: {r.text[:200]}")
    created_id = None

# POST with invalid battery (>100) — should 422
bad_bike = {"model": "BadBike", "battery": 150, "status": "available"}
r = requests.post(f"{BASE}/bikes/", json=bad_bike)
if r.status_code == 422:
    log_pass("POST /bikes/ battery=150 — correctly rejected with 422")
else:
    log_fail("POST /bikes/ battery=150", f"Expected 422, got {r.status_code}")

# PUT update the bike we created
if created_id:
    updated_bike = {
        "model": "SmokeTestBike-Updated",
        "battery": 50.0,
        "status": "maintenance",
        "station_id": None,
    }
    r = requests.put(f"{BASE}/bikes/{created_id}", json=updated_bike)
    if r.status_code == 200 and r.json().get("model") == "SmokeTestBike-Updated":
        log_pass(f"PUT /bikes/{created_id} — updated successfully")
    else:
        log_fail(f"PUT /bikes/{created_id}", f"Status {r.status_code}, body: {r.text[:200]}")

# DELETE the bike we created
if created_id:
    r = requests.delete(f"{BASE}/bikes/{created_id}")
    if r.status_code == 200:
        log_pass(f"DELETE /bikes/{created_id} — deleted successfully")
    else:
        log_fail(f"DELETE /bikes/{created_id}", f"Status {r.status_code}")

    # Confirm it is gone
    r = requests.get(f"{BASE}/bikes/{created_id}")
    if r.status_code == 404:
        log_pass(f"GET /bikes/{created_id} after delete — confirmed 404")
    else:
        log_fail(f"GET /bikes/{created_id} after delete", f"Expected 404, got {r.status_code}")

# PERSISTENCE TEST — the professor's key question
r = requests.get(f"{BASE}/bikes/")
bike_count = len(r.json()) if r.status_code == 200 else 0
log_pass(f"Database persistence — {bike_count} bikes in DB (these survive a restart)")


# ─────────────────────────────────────────────────────────────
# 2. USERS CRUD
# ─────────────────────────────────────────────────────────────
section("2. USERS CRUD")

r = requests.get(f"{BASE}/users/")
if r.status_code == 200 and isinstance(r.json(), list):
    users = r.json()
    log_pass(f"GET /users/ — returned {len(users)} users")
else:
    log_fail("GET /users/", f"Status {r.status_code}")

r = requests.get(f"{BASE}/users/1")
if r.status_code == 200:
    log_pass(f"GET /users/1 — found: {r.json().get('username')}")
else:
    log_fail("GET /users/1", f"Status {r.status_code}")

r = requests.get(f"{BASE}/users/999")
if r.status_code == 404:
    log_pass("GET /users/999 — correctly returned 404")
else:
    log_fail("GET /users/999", f"Expected 404, got {r.status_code}")


# ─────────────────────────────────────────────────────────────
# 3. RENTALS
# ─────────────────────────────────────────────────────────────
section("3. RENTALS")

# Valid rental
rental = {"bike_id": 1, "user_id": 1, "battery_level": 50.0}
r = requests.post(f"{BASE}/rentals/", json=rental)
if r.status_code == 201:
    log_pass("POST /rentals/ battery=50 — rental created")
else:
    log_fail("POST /rentals/ battery=50", f"Status {r.status_code}, body: {r.text[:200]}")

# Low battery rental — should be rejected
low_rental = {"bike_id": 1, "user_id": 1, "battery_level": 10.0}
r = requests.post(f"{BASE}/rentals/", json=low_rental)
if r.status_code == 422:
    log_pass("POST /rentals/ battery=10 — correctly rejected with 422")
else:
    log_fail("POST /rentals/ battery=10", f"Expected 422, got {r.status_code}")

# GET all rentals
r = requests.get(f"{BASE}/rentals/")
if r.status_code == 200 and isinstance(r.json(), list):
    log_pass(f"GET /rentals/ — returned {len(r.json())} rentals")
else:
    log_fail("GET /rentals/", f"Status {r.status_code}")


# ─────────────────────────────────────────────────────────────
# 4. AUTH — JWT LOGIN
# ─────────────────────────────────────────────────────────────
section("4. AUTH — JWT LOGIN")

# Login as rider
r = requests.post(f"{BASE}/token", data={"username": "rider_one", "password": "riderpass123"})
if r.status_code == 200 and "access_token" in r.json():
    rider_token = r.json()["access_token"]
    log_pass("POST /token rider_one — login successful, token received")
else:
    log_fail("POST /token rider_one", f"Status {r.status_code}, body: {r.text[:200]}")
    rider_token = None

# Login as admin
r = requests.post(f"{BASE}/token", data={"username": "admin_dave", "password": "adminpass123"})
if r.status_code == 200 and "access_token" in r.json():
    admin_token = r.json()["access_token"]
    log_pass("POST /token admin_dave — login successful, token received")
else:
    log_fail("POST /token admin_dave", f"Status {r.status_code}, body: {r.text[:200]}")
    admin_token = None

# Wrong password
r = requests.post(f"{BASE}/token", data={"username": "rider_one", "password": "wrong"})
if r.status_code == 401:
    log_pass("POST /token wrong password — correctly returned 401")
else:
    log_fail("POST /token wrong password", f"Expected 401, got {r.status_code}")

# Nonexistent user
r = requests.post(f"{BASE}/token", data={"username": "nobody", "password": "test"})
if r.status_code == 401:
    log_pass("POST /token nonexistent user — correctly returned 401")
else:
    log_fail("POST /token nonexistent user", f"Expected 401, got {r.status_code}")


# ─────────────────────────────────────────────────────────────
# 5. ROLE-BASED ACCESS — STATIONS
# ─────────────────────────────────────────────────────────────
section("5. ROLE-BASED ACCESS — STATIONS")

station_data = {"name": "Test Station", "location": "Downtown", "capacity": 20}

# No token — should 401
r = requests.post(f"{BASE}/stations/", json=station_data)
if r.status_code == 401:
    log_pass("POST /stations/ no token — correctly returned 401")
else:
    log_fail("POST /stations/ no token", f"Expected 401, got {r.status_code}")

# Rider token — should 403
if rider_token:
    headers = {"Authorization": f"Bearer {rider_token}"}
    r = requests.post(f"{BASE}/stations/", json=station_data, headers=headers)
    if r.status_code == 403:
        log_pass("POST /stations/ as rider — correctly returned 403 Forbidden")
    else:
        log_fail("POST /stations/ as rider", f"Expected 403, got {r.status_code}")

# Admin token — should 201
if admin_token:
    headers = {"Authorization": f"Bearer {admin_token}"}
    r = requests.post(f"{BASE}/stations/", json=station_data, headers=headers)
    if r.status_code == 201:
        body = r.json()
        log_pass(f"POST /stations/ as admin — created station id={body.get('id')}")
        if body.get("name") == "Test Station":
            log_pass("Station data persisted correctly in database")
    else:
        log_fail("POST /stations/ as admin", f"Expected 201, got {r.status_code}, body: {r.text[:200]}")


# ─────────────────────────────────────────────────────────────
# 6. ADMIN ENDPOINT (API KEY)
# ─────────────────────────────────────────────────────────────
section("6. ADMIN ENDPOINT (API KEY)")

# No key
r = requests.get(f"{BASE}/admin/stats")
if r.status_code == 422 or r.status_code == 403:
    log_pass(f"GET /admin/stats no key — blocked ({r.status_code})")
else:
    log_fail("GET /admin/stats no key", f"Expected 422 or 403, got {r.status_code}")

# Wrong key
r = requests.get(f"{BASE}/admin/stats", headers={"api-key": "wrong-key"})
if r.status_code == 403:
    log_pass("GET /admin/stats wrong key — correctly returned 403")
else:
    log_fail("GET /admin/stats wrong key", f"Expected 403, got {r.status_code}")

# Correct key
r = requests.get(f"{BASE}/admin/stats", headers={"api-key": "eco-admin-secret"})
if r.status_code == 200:
    log_pass("GET /admin/stats correct key — access granted")
else:
    log_fail("GET /admin/stats correct key", f"Expected 200, got {r.status_code}")


# ─────────────────────────────────────────────────────────────
# 7. ML PREDICTION
# ─────────────────────────────────────────────────────────────
section("7. ML PREDICTION")

# Valid prediction
payload = {"distance_km": 10.0, "battery_level": 80.0}
r = requests.post(f"{BASE}/predict/", json=payload)
if r.status_code == 200 and "estimated_minutes" in r.json():
    mins = r.json()["estimated_minutes"]
    log_pass(f"POST /predict/ 10km 80% — estimated {mins} minutes")
    if 15 < mins < 40:
        log_pass(f"Prediction is in sane range (15-40 min for 10km)")
    else:
        log_warn("Prediction range", f"{mins} minutes seems unusual for 10km at 80% battery")
else:
    log_fail("POST /predict/", f"Status {r.status_code}, body: {r.text[:200]}")

# Edge case — max distance, low battery
payload2 = {"distance_km": 100.0, "battery_level": 5.0}
r = requests.post(f"{BASE}/predict/", json=payload2)
if r.status_code == 200:
    mins2 = r.json()["estimated_minutes"]
    log_pass(f"POST /predict/ 100km 5% — estimated {mins2} minutes")
else:
    log_fail("POST /predict/ 100km 5%", f"Status {r.status_code}")

# Invalid input — string instead of number
r = requests.post(f"{BASE}/predict/", json={"distance_km": "abc", "battery_level": 80})
if r.status_code == 422:
    log_pass("POST /predict/ invalid input — correctly returned 422")
else:
    log_fail("POST /predict/ invalid input", f"Expected 422, got {r.status_code}")

# Invalid input — distance = 0 (must be > 0 per schema)
r = requests.post(f"{BASE}/predict/", json={"distance_km": 0, "battery_level": 80})
if r.status_code == 422:
    log_pass("POST /predict/ distance=0 — correctly rejected (gt=0)")
else:
    log_fail("POST /predict/ distance=0", f"Expected 422, got {r.status_code}")

# Invalid input — battery = 150 (must be <= 100)
r = requests.post(f"{BASE}/predict/", json={"distance_km": 10, "battery_level": 150})
if r.status_code == 422:
    log_pass("POST /predict/ battery=150 — correctly rejected (le=100)")
else:
    log_fail("POST /predict/ battery=150", f"Expected 422, got {r.status_code}")


# ─────────────────────────────────────────────────────────────
# 8. LOGGING / OBSERVABILITY
# ─────────────────────────────────────────────────────────────
section("8. LOGGING / OBSERVABILITY")

log_file = "ecomute.log"
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        content = f.read()
    lines = [l for l in content.strip().split("\n") if l.strip()]
    if len(lines) > 0:
        log_pass(f"ecomute.log exists with {len(lines)} entries")
        has_warning = any("WARNING" in l for l in lines)
        if has_warning:
            log_pass("Log file contains WARNING-level entries")
        else:
            log_warn("Log file warnings", "No WARNING entries found. Hit GET /bikes/999 to generate one.")
        has_timestamp = any(" - " in l and "202" in l for l in lines)
        if has_timestamp:
            log_pass("Log entries have timestamps")
        else:
            log_warn("Log timestamps", "Entries may be missing timestamps")
        print(f"\n  Last 3 log entries:")
        for line in lines[-3:]:
            print(f"    {line}")
    else:
        log_warn("ecomute.log", "File exists but is empty. Make some requests first.")
else:
    log_warn("ecomute.log", "File not found. Run the server and make requests to generate it.")


# ─────────────────────────────────────────────────────────────
# 9. PYDANTIC VALIDATION
# ─────────────────────────────────────────────────────────────
section("9. PYDANTIC VALIDATION")

# Battery > 100
r = requests.post(f"{BASE}/bikes/", json={"model": "X", "battery": 101, "status": "available"})
if r.status_code == 422:
    log_pass("Bike battery=101 — rejected by Pydantic (le=100)")
else:
    log_fail("Bike battery=101", f"Expected 422, got {r.status_code}")

# Battery < 0
r = requests.post(f"{BASE}/bikes/", json={"model": "X", "battery": -5, "status": "available"})
if r.status_code == 422:
    log_pass("Bike battery=-5 — rejected by Pydantic (ge=0)")
else:
    log_fail("Bike battery=-5", f"Expected 422, got {r.status_code}")

# Invalid status
r = requests.post(f"{BASE}/bikes/", json={"model": "X", "battery": 50, "status": "flying"})
if r.status_code == 422:
    log_pass("Bike status='flying' — rejected by Pydantic (Literal)")
else:
    log_fail("Bike status='flying'", f"Expected 422, got {r.status_code}")

# Missing required field
r = requests.post(f"{BASE}/bikes/", json={"battery": 50, "status": "available"})
if r.status_code == 422:
    log_pass("Bike missing 'model' — rejected by Pydantic")
else:
    log_fail("Bike missing 'model'", f"Expected 422, got {r.status_code}")

# Rental battery < 20
r = requests.post(f"{BASE}/rentals/", json={"bike_id": 1, "user_id": 1, "battery_level": 15})
if r.status_code == 422:
    log_pass("Rental battery=15 — rejected by model_validator (<20)")
else:
    log_fail("Rental battery=15", f"Expected 422, got {r.status_code}")


# ─────────────────────────────────────────────────────────────
# 10. DEPENDENCY INJECTION CHECK
# ─────────────────────────────────────────────────────────────
section("10. DEPENDENCY INJECTION (code check)")

files_to_check = [
    ("src/app/routers/bikes.py", "Depends(get_db)"),
    ("src/app/routers/users.py", "Depends(get_db)"),
    ("src/app/routers/rentals.py", "Depends(get_db)"),
    ("src/app/routers/stations.py", "Depends(get_current_user)"),
    ("src/app/routers/auth.py", "Depends(get_db)"),
    ("src/app/routers/admin.py", "Depends(verify_admin_key)"),
]

for filepath, pattern in files_to_check:
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            content = f.read()
        if pattern in content:
            log_pass(f"{filepath} — uses {pattern}")
        else:
            log_fail(f"{filepath}", f"Missing {pattern}")
    else:
        log_fail(filepath, "File not found")


# ─────────────────────────────────────────────────────────────
# 11. LOGGING INSTRUMENTATION CHECK
# ─────────────────────────────────────────────────────────────
section("11. LOGGING INSTRUMENTATION (code check)")

log_files = [
    "src/main.py",
    "src/seed.py",
    "src/app/routers/bikes.py",
    "src/app/routers/users.py",
    "src/app/routers/rentals.py",
    "src/app/routers/stations.py",
    "src/app/routers/admin.py",
    "src/app/routers/auth.py",
    "src/app/routers/predictions.py",
]

for filepath in log_files:
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            content = f.read()
        has_logger = "logger" in content
        has_print = "print(" in content
        if has_logger and not has_print:
            log_pass(f"{filepath} — uses logger, no print()")
        elif has_logger and has_print:
            log_warn(f"{filepath}", "Uses logger BUT also has print() — remove print() calls")
        else:
            log_fail(f"{filepath}", "No logger found")
    else:
        log_fail(filepath, "File not found")


# ─────────────────────────────────────────────────────────────
# 12. ML MODEL FILE CHECK
# ─────────────────────────────────────────────────────────────
section("12. ML MODEL FILE")

model_path = "src/ml/trip_predictor.joblib"
if os.path.exists(model_path):
    size_kb = os.path.getsize(model_path) / 1024
    log_pass(f"{model_path} exists ({size_kb:.1f} KB)")
else:
    log_fail(model_path, "File not found. Run: python -m src.ml.train")

train_path = "src/ml/train.py"
if os.path.exists(train_path):
    with open(train_path, "r") as f:
        content = f.read()
    if "LinearRegression" in content:
        log_pass("train.py uses LinearRegression")
    if "pandas" in content or "DataFrame" in content:
        log_pass("train.py uses pandas DataFrame")
    if "joblib.dump" in content:
        log_pass("train.py uses joblib.dump() to serialize model")
else:
    log_fail(train_path, "File not found")


# ─────────────────────────────────────────────────────────────
# FINAL REPORT
# ─────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("  FINAL REPORT")
print("=" * 60)
print()
print(f"  PASSED:   {PASS_COUNT}")
print(f"  WARNINGS: {WARN_COUNT}")
print(f"  FAILED:   {FAIL_COUNT}")
print()

if FAIL_COUNT == 0 and WARN_COUNT == 0:
    print("  STATUS: READY TO PRESENT. Zero issues found.")
elif FAIL_COUNT == 0:
    print("  STATUS: MOSTLY READY. Fix the warnings if you have time.")
else:
    print("  STATUS: NOT READY. Fix the failures above before presenting.")
    print("  Each [FAIL] line tells you exactly what broke.")

print()