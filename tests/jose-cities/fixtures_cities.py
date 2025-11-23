


new_city_payload = {
    "type": "Feature",
    "properties": {
        "name": "Test City",
        "population": 12345
    },
    "geometry": {
        "type": "Point",
        "coordinates": [-46.6333, -23.5505] 
    }
}

updated_city_payload = {
    "type": "Feature",
    "properties": {
        "name": "Updated City",
        "population": 54321
    },
    "geometry": {
        "type": "Point",
        "coordinates": [-46.634, -23.551]
    }
}

partial_update_payload = {
    "properties": {
        "population": 99999
    }
}
