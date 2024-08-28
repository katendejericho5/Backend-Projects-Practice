import requests
import json

# Make the GET request to the horoscope API
response = requests.get("https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign=capricorn&day=today")
data = response.json()  # Convert the response to JSON

# Store the JSON data in a file
with open("horoscope_data.json", "w") as file:
    json.dump(data, file)

print("Data stored successfully!")

# Retrieve JSON data from the file
with open("horoscope_data.json", "r") as file:
    data = json.load(file)

# Access and process the retrieved JSON data
date = data["data"]["date"]
horoscope_data = data["data"]["horoscope_data"]

# Print the retrieved data
print(f"Horoscope for date {date}: {horoscope_data}")


# Retrieve JSON data from the file
with open("horoscope_data.json", "r") as file:
    data = json.load(file)

# Format the data
formatted_data = json.dumps(data, indent=2)

print(formatted_data)