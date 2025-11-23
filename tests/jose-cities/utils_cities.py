

import requests

BASE_URL = "https://fooapi.com/api/cities"

def get_all_cities(params=None):
    return requests.get(BASE_URL, params=params)

def get_city_by_id(city_id):
    return requests.get(f"{BASE_URL}/{city_id}")

def get_random_city():
    return requests.get(f"{BASE_URL}/rand")

def create_city(payload):
    return requests.post(BASE_URL, json=payload)

def update_city(city_id, payload):
    return requests.put(f"{BASE_URL}/{city_id}", json=payload)

def patch_city(city_id, payload):
    return requests.patch(f"{BASE_URL}/{city_id}", json=payload)

def delete_city(city_id):
    return requests.delete(f"{BASE_URL}/{city_id}")
