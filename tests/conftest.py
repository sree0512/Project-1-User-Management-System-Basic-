# import sys
# import os
import pytest

# -----------------------------------------
# Add project root to Python path
# This ensures 'import app' works from tests/
# -----------------------------------------
# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# if PROJECT_ROOT not in sys.path:
#     sys.path.append(PROJECT_ROOT)

# -----------------------------------------
# Import Flask app factory after fixing path
# -----------------------------------------
from app import create_app

# -----------------------------------------
# Pytest fixture to provide test client
# -----------------------------------------
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

        
        
"""
Project1/
├─ app/
│   ├─ __init__.py
│   ├─ config.py
│   ├─ db.py
│   ├─ models.py
│   └─ services/
├─ scripts/
├─ tests/
│   ├─ conftest.py
│   ├─ test_auth.py
│   └─ test_user.py
├─ requirements.txt
└─ ...

"""