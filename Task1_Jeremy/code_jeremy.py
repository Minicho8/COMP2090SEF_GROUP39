import math
# Model for representing the distance of the location
class Location:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
    def distance_km_to(self, other: "Location") -> float:
        # Haversine formula determines the great-circle distance between two points on a sphere given their longitudes and latitudes
        earth_radius = 6371  
        lat1 = math.radians(self.latitude)
        lat2 = math.radians(other.latitude)
        lon1 = math.radians(self.longitude)
        lon2 = math.radians(other.longitude)
    
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance_km = earth_radius * c
        return distance_km    
test_1 = Location("Current", 22.3069, 114.1750) 

test_2 = Location("Restaurant", 22.3195, 114.1751)

distance_km = test_1.distance_km_to(test_2)
print(f"The distance is {distance_km:.2f} km")
