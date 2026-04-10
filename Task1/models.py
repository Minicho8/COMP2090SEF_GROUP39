import math,time
from datetime import datetime

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

        if start_location == None:
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
        ''',Location(22.31731238014429, 114.1746904182537,'zone1b')'''
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

class WeeklyHours:
    def __init__(self):
        pass

    def today_time(self):
        self.today_week = int(datetime.now().strftime("%w"))
        self.now_time = datetime.now().time()
        #print(self.today_week,self.now_time)

    @staticmethod
    def parse_hours(hours_str):
        hours_obj = {}
        # Remove 'hours = ' and strip whitespace
        
        hours_str = hours_str.replace('–', '-')
        cleaned_str = hours_str.replace("hours = ", "").strip('"')
        # split by ; to get days
        #print(60,cleaned_str)
        days = cleaned_str.split(';')
        #print(62,days)
        for day_range in days:
            # if '=' not in day_range: continue
            #print(65,day_range)
            day, times = day_range.split('=')
            day = day.strip()
            times = times.strip()
            #print(69,day, times)
            if times.lower() == 'closed':
                hours_obj[day] = []
            else:
                # handle multiple time ranges (/ separated)
                range_list = []
                for r in times.split('/'):
                    start, end = r.split('-')
                    #print(start.strip(), end.strip())
                    range_list.append((
                        datetime.strptime(start.strip(), "%H:%M").time(),
                        datetime.strptime(end.strip(), "%H:%M").time()
                    ))
                hours_obj[day] = range_list
            #print(83,hours_obj)
        return hours_obj
    @staticmethod
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
    def __init__(self, id=None, name=None, location=None, address=None, cuisines=None, price_level=None, rating=None, dietary_tags=None, weekly_hours=None, stu_discount=None, phone=None, website=None, google_map=None):
        self.id = id
        self.name = name
        self.address = address
        self.location = location
        self.cuisines = cuisines
        self.price_level = price_level
        self.rating = rating
        self.dietary_tags = dietary_tags
        self.weekly_hours = weekly_hours
        self.stu_discount = stu_discount
        self.phone = phone
        self.website = website
        self.google_map = google_map

