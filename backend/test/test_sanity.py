import pytest

def test_simple():
    """Simple test to verify pytest is working."""
    assert True

def test_import_app():
    """Test that we can import the app without AWS issues."""
    try:
        from test_app_setup import app
        assert app is not None
    except Exception as e:
        pytest.fail(f"Failed to import app: {e}") 