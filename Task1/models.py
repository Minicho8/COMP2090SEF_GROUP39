import math,datetime

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
    def __init__(self,id):
        self.name = id.name
        self.hours = id.weekly_hours

    def today_time(self):
        self.today_week = int(datetime.datetime.now().strftime("%w"))
        self.now_time = datetime.datetime.now().time()
        print(self.today_week,self.now_time)

    def restaurant_opening_hours(self):
        a = self.hours[self.today_week].split('-')
        opening_hour = datetime.datetime.strptime(a[0],"%H:%M").time()
        closing_hour = datetime.datetime.strptime(a[1],"%H:%M").time()
        today_date = datetime.datetime.now().date()
        closing_datetime = datetime.datetime.combine(today_date, closing_hour)
        last_time = (closing_datetime - datetime.timedelta(minutes=30)).time()
        print(today_date,closing_datetime,last_time)
        print(opening_hour,closing_hour)

        if opening_hour <= self.now_time <= closing_hour:
            if self.now_time >= last_time:
                print("nearly last order / closing")
            return True
        else:
            return False


class Restaurant:
# id,name,address,lat,lon,cuisines,price_level,dietary_tags,rating,hours,stu_discount,phone,wesite1,website, ,google_map

    def __init__(self, id, name, location, cuisines, price_level, rating, dietary_tags, weekly_hours):
        self.id = id
        self.name = name
        self.location = location
        self.cuisines = cuisines
        self.price_level = price_level
        self.rating = rating
        self.dietary_tags = dietary_tags
        self.weekly_hours = weekly_hours

