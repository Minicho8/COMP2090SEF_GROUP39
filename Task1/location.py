import math
from abc import ABC, abstractmethod
class Location:
    def __init__(self, lat, lon, name=None):
        self.lat = lat
        self.lon = lon
        self.name = name
    def distance_km_from(self, other_location: 'Location', start_location: 'Location' = None, step=None) -> float:
        if step is None:
            step = []

        earth_radius = 6371.0 

        lat_start = self.lat
        lat_end = other_location.lat
        
        lon_start = self.lon
        lon_end = other_location.lon

        distance_lat = math.radians(lat_end - lat_start)
        distance_lon = math.radians(lon_end - lon_start)

        a = math.sin(distance_lat / 2)**2 + math.cos(math.radians(lat_start)) * math.cos(math.radians(lat_end)) * math.sin(distance_lon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance_km = earth_radius * c

        if start_location is None:
            print('in check g pt')
            min_d = 0
            gather_points = self.get_gather_points(step)
            for loc in gather_points:
                temp = self.distance_km_from(other_location=loc,start_location=other_location)
                if min_d == 0:
                    min_d = temp
                    curr_pt = loc
                elif temp < min_d:
                    min_d = temp
                    curr_pt = loc
            if min_d != 0 and min_d < distance_km:
                step.append(curr_pt.name)
                distance_km = min_d 
                distance_km += curr_pt.distance_km_from(other_location, step=step)
            else:
                print('x check inner g pt', distance_km , step)
        return distance_km
    @staticmethod
    def get_gather_points(used_pts):
        remain_points =[]
        gather_points = [Location(22.317397423147696, 114.1781050172544,'midcross'),
                         Location(22.318306263322874, 114.17556076825,'zone1a'),
                         Location(22.313979928254117, 114.17788097976785,'zone2a')]
        if len(used_pts) > 0:
            for loc in gather_points:
                if loc.name in used_pts:
                    pass
                else:
                    remain_points.append(loc)
        else:
            remain_points = gather_points
        return remain_points
  
class EstimatedWalkingtime:
    def __init__(self, walking_speed= 4.3):
        self.walking_speed = walking_speed 
    
    def estimated_walking_time(self, distance_km: float):
        time_hr = distance_km / self.walking_speed
        return math.ceil(time_hr * 60)

class Campus:
    def __init__(self):
        self.___locations = {
            "MC": Location(22.316436688553082, 114.18027979232998),
            "IOH": Location(22.317460480368453, 114.17972807484017),
            "JCC": Location(22.31584884625968, 114.17819153494024),
            "HMT_PLAZA": Location(22.316643582001106, 114.18181510911974)
        }
    def get_campus(self, campus_name):
        return self.___locations.get(campus_name.upper())



