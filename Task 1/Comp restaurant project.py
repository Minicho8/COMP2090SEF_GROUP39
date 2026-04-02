import math
# Function for calculating the distance of the chosen campus to location
class Location:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
    def distance_km_to(self, other: "Location") -> float:
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
test_1 = Location("Campus", 22.3069, 114.1750) 
test_2 = Location("Restaurant", 22.3195, 114.1751)

distance_km = test_1.distance_km_to(test_2)
print(f"The distance is {distance_km:.2f} km")

# Searching users current location(campus)
class Campus:
    def __init__(self, name, location):
        self.name = name
        self.location = location
    def current_campus(campus_name):
        MC = Location("Campus", 22.316436688553082, 114.18027979232998)
        IOH = Location("Campus", 22.317460480368453, 114.17972807484017)
        JCC = Location("Campus", 22.315821729082074, 114.17817511793885)
        HMT_plaza = Location("Campus", 22.316643582001106, 114.18181510911974)




#main campus : 22.316436688553082, 114.18027979232998
#ioh : 22.317460480368453, 114.17972807484017
#JCC : 22.315821729082074, 114.17817511793885
#ho man tin plaza : 22.316643582001106, 114.18181510911974





class EstimatiedWalkingTime:
    def __init__(self, ):


    def estimated_walking_time():
        
