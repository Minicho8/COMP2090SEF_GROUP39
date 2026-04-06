import math

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
  
class EstimatedWalkingtime:
    def __init__(self, walking_speed= 5.0):
        self.walking_speed = walking_speed 
    
    def estimated_walking_time(self, distance_km: float):
        time_hr = distance_km / self.walking_speed
        return time_hr * 60

class Campus:
    def __init__(self):
        self.locations = {
            "MC": Location("Main Campus", 22.316436688553082, 114.18027979232998),
            "IOH": Location("IOH", 22.317460480368453, 114.17972807484017),
            "JCC": Location("JCC", 22.315821729082074, 114.17817511793885),
            "HMT_PLAZA": Location("Ho Man Tin Plaza", 22.316643582001106, 114.18181510911974)
        }
    def get_campus(self, campus_name):
        return self.locations.get(campus_name.upper())

class WeeklyHours:
    pass
class Restaurant:
    pass