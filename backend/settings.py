import os


SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", default="sqlite:///./db.sqlite3")

LOGISTICS_A_URL = os.getenv("LOGISTICS_A_URL", "http://localhost:8001/api/logistics-a")
LOGISTICS_B_URL = os.getenv("LOGISTICS_B_URL", "http://localhost:8002/api/logistics-b")
