import pytest
import requests

@pytest.fixture
def base_url():
    return "https://fooapi.com/api"  

@pytest.fixture
def headers():
 
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
