import requests

data = {
    "url": "http://127.0.0.1:8001/ping",
    "delay": 5,
    "id": "test-job"
}

response = requests.post("http://127.0.0.1:8001/set-timer", json=data)

print(response.json())
