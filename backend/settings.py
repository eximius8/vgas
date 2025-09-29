import os

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", default="sqlite:///./db.sqlite3")

LOGISTICS_A_URL = os.getenv("LOGISTICS_A_URL", "http://localhost:8001/api/logistics-a")
LOGISTICS_B_URL = os.getenv("LOGISTICS_B_URL", "http://localhost:8002/api/logistics-b")