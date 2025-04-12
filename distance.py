import math
from dotenv import load_dotenv
import os
import requests
import csv

#MELISSA KEY
load_dotenv()
license_key = os.getenv("MELISSA_API_KEY")


# def get_coordinates(address, city, state, postal, license_key):
#     url = "https://address.melissadata.net/v3/WEB/GlobalAddress/doGlobalAddress"
#     params = {
#         "id": license_key,
#         "a1": address,
#         "loc": city,
#         "admarea": state,
#         "postal": postal,
#         "ctry": "USA",  # Default to USA
#         "opt": "OutputGeo:ON"
#     }

#     response = requests.get(url, params=params)
#     data = response.json()

#     try:
#         record = data['Records'][0]
#         lat = float(record['Latitude'])
#         lon = float(record['Longitude'])
#         return (lat, lon)
#     except Exception as e:
#         print("Error getting coordinates for:", address, city, state, postal)
#         print("Details:", e)
#         print("Response:", data)
#         return None


#DISTANCE FORMULA
def degrees_to_radians(deg):
    return deg / 57.3  # Melissa's recommended constant

def exact_distance(lat1, lon1, lat2, lon2):
    # Convert degrees to radians using Melissa's method
    lat1_rad = degrees_to_radians(lat1)
    lon1_rad = degrees_to_radians(lon1)
    lat2_rad = degrees_to_radians(lat2)
    lon2_rad = degrees_to_radians(lon2)

    A = math.sin(lat1_rad) * math.sin(lat2_rad) + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.cos(lon2_rad - lon1_rad)

    distance = 3959 * math.atan2(math.sqrt(1 - A**2), A)  # Earth radius in miles
    return distance

# Coordinates: UCI to Disneyland as a test
# lat_uci, lon_uci = 33.6405, -117.8443
# lat_disney, lon_disney = 33.8121, -117.9190

# print("Exact Distance (miles):", exact_distance(lat_uci, lon_uci, lat_disney, lon_disney))
# print("Approximate Distance (miles):", exact_distance(lat_uci, lon_uci, lat_disney, lon_disney))

# CSV reading and distance calculation
with open("Addresses.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    i=1
    for row in reader:
        i+=1
        address = row['Address']
        Latitude = row['Latitude']
        Longitude = row['Longitude']

        # coords = get_coordinates(address, city, state, postal, license_key)
        
        print(i,".",address,",",Latitude,",",Longitude)


        # if coords:
        #     lat, lon = coords
        #     dist = exact_distance(lat, lon)
        #     print(f"{address}, {city}, {state} {postal} → {dist:.2f} miles")
        # else:
        #     print(f"Could not get coordinates for {address}")