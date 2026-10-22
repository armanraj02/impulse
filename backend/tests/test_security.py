from fastapi.testclient import TestClient
from sqlalchemy.exc import ProgrammingError, InternalError
from sqlalchemy import text
import pytest
from app.main import app
from app.database import SessionLocal

def test_readonly_user():
    # Attempt to write to the database
    db = SessionLocal()
    try:
        # Try to insert into department_performance_summary
        db.execute(text("INSERT INTO department_performance_summary (department_code) VALUES ('TEST')"))
        db.commit()
        assert False, "Should have raised an exception"
    except Exception as e:
        # Expecting a permission denied error
        assert "permission denied" in str(e).lower()
        db.rollback()
    finally:
        db.close()
