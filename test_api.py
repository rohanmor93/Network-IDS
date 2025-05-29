import requests

url = "http://127.0.0.1:5000/predict"

# ⚠️ Now only 41 values
data = {
    "features": [
        0, 0, 3, 181, 5450, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0
    ]
}

response = requests.post(url, json=data)
print(response.json())
