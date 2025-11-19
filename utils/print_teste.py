import json
def print_response_body(response):
    try:
        body = response.json()
        pretty = json.dumps(body, indent=2, ensure_ascii=False)  
        print("Response JSON body:\n" + pretty)
    except Exception:
        print("Response text body:\n" + (response.text or "<empty>"))