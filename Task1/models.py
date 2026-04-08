import math
from datetime import datetime

class Location:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
    def distance_km_to(loc1, loc2) -> float:
        earth_radius = 6371  
        lat_start = math.radians(loc1.lat)
        lon_start = math.radians(loc1.lon)

        lat_end = math.radians(loc2.lat)
        lon_end = math.radians(loc2.lon)
    
        distance_lat = lat_end - lat_start
        distance_lon = lon_end - lon_start

        a = math.sin(distance_lat / 2) ** 2 + math.cos(lat_start) * math.cos(lat_end) * math.sin(distance_lon/2) ** 2
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
        self.___locations = {
            "MC": Location("Main Campus", 22.316436688553082, 114.18027979232998),
            "IOH": Location("IOH", 22.317460480368453, 114.17972807484017),
            "JCC": Location("JCC", 22.315821729082074, 114.17817511793885),
            "HMT_PLAZA": Location("Ho Man Tin Plaza", 22.316643582001106, 114.18181510911974)
        }
    def get_campus(self, campus_name):
        return self.___locations.get(campus_name.upper())

class WeeklyHours:
    def __init__(self):
        pass

    def today_time(self):
        self.today_week = int(datetime.now().strftime("%w"))
        self.now_time = datetime.now().time()
        print(self.today_week,self.now_time)

    def parse_hours(hours_str):
        hours_obj = {}
        # Remove 'hours = ' and strip whitespace
        
        hours_str = hours_str.replace('–', '-')
        cleaned_str = hours_str.replace("hours = ", "").strip('"')
        # split by ; to get days
        print(60,cleaned_str)
        days = cleaned_str.split(';')
        print(62,days)
        for day_range in days:
            # if '=' not in day_range: continue
            print(65,day_range)
            day, times = day_range.split('=')
            day = day.strip()
            times = times.strip()
            print(69,day, times)
            if times.lower() == 'closed':
                hours_obj[day] = []
            else:
                # handle multiple time ranges (/ separated)
                range_list = []
                for r in times.split('/'):
                    start, end = r.split('-')
                    print(start.strip(), end.strip())
                    range_list.append((
                        datetime.strptime(start.strip(), "%H:%M").time(),
                        datetime.strptime(end.strip(), "%H:%M").time()
                    ))
                hours_obj[day] = range_list
            print(83,hours_obj)
        return hours_obj
    
    def textformat(schedule):
        formatted_output = []
        for day, intervals in schedule.items():
            # Capitalize the day (e.g., 'mon' -> 'Mon')
            day_name = day.capitalize()
            
            if not intervals:
                status = "Closed"
            else:
                # Join multiple time slots with a comma (e.g., 07:00-15:00, 16:00-22:00)
                status = ", ".join([f"{start.strftime('%H:%M')}-{end.strftime('%H:%M')}" for start, end in intervals])
            formatted_output.append(f"{day_name}: {status}")
        return "\n".join(formatted_output)
    
    # def restaurant_opening_hours(self):
    #     a = self.hours[self.today_week].split('-')
    #     opening_hour = datetime.datetime.strptime(a[0],"%H:%M").time()
    #     closing_hour = datetime.datetime.strptime(a[1],"%H:%M").time()
    #     today_date = datetime.datetime.now().date()
    #     closing_datetime = datetime.datetime.combine(today_date, closing_hour)
    #     last_time = (closing_datetime - datetime.timedelta(minutes=30)).time()
    #     print(today_date,closing_datetime,last_time)
    #     print(opening_hour,closing_hour)

    #     if opening_hour <= self.now_time <= closing_hour:
    #         if self.now_time >= last_time:
    #             print("near last order / closing")
    #         return True
    #     else:
    #         return False


class Restaurant:
# id,name,address,lat,lon,cuisines,price_level,dietary_tags,rating,hours,stu_discount,phone,wesite1,website, ,google_map
    def __init__(self, id=None, name=None, location=None, lat=None, lon=None, cuisines=None, price_level=None, rating=None, dietary_tags=None, weekly_hours=None, stu_discount=None, phone=None, website=None, google_map=None):
        self.id = id
        self.name = name
        self.location = location
        self.lat = lat
        self.lon = lon
        self.cuisines = cuisines
        self.price_level = price_level
        self.rating = rating
        self.dietary_tags = dietary_tags
        self.weekly_hours = weekly_hours
        self.stu_discount = stu_discount
        self.phone = phone
        self.website = website
        self.google_map = google_map

