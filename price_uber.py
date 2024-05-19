import json

import requests

# Replace these with your actual values
start_latitude = 37.7752315
end_latitude = 37.7899886
start_longitude = -122.4197514
end_longitude = -122.4089156
access_token = "CB5oo2VkxrTzAT_ArNI4QuAqzVITXd0ZyRdwSq4a"

url = "https://api.uber.com/v1/guests/trips/estimates"

payload = {
    "pickup": {"latitude": start_latitude, "longitude": start_longitude},
    "dropoff": {"latitude": end_latitude, "longitude": end_longitude},
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + access_token,
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.text)
