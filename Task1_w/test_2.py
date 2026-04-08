class CsvRestaurantRepository():
# id,name,location,lat,lon,cuisines,price_level,dietary_tags,rating,weekly_hours,stu_discount,phone,website,google_map

    def __init__(self):
        self.restaurant_list = []


    def read_file(self):
        file = open('restaurants.csv','r', encoding='utf-8', errors='replace')
        file_lines = file.readlines()
        file.close()
        
        for each in file_lines:
            item = each.strip().split(',')
            item[13:15] = [','.join(item[13:15])]
            self.id = item[0]
            self.name = item[1]
            self.location = item[2]
            self.lat = item[3]
            self.lon = item[4]
            self.cuisines = item[5]
            self.price_level = item[6]
            self.dietary_tags = item[7]
            self.rating = item[8]
            self.weekly_hours = item[9]
            self.stu_discount = item[10]
            self.phone = item[11]
            self.website = item[12]
            self.google_map = item[13]
            #print(item)

            self.fix_format()


            restaurant_obj = Restaurant(self.id,self.name,self.location,self.lat,self.lon,self.cuisines,self.price_level,self.dietary_tags,self.rating,self.weekly_hours,self.stu_discount,self.phone,self.website,self.google_map)

            self.restaurant_list.append(restaurant_obj)
        
    def fix_format(self):
        self.id = int(self.id)
        self.location = self.location.replace(';',',')

        self.lat = float(self.lat)
        self.lon = float(self.lon)
        fix_num = lambda x : 0 if x == "/" else int(x)
        self.price_level = fix_num(self.price_level)
        self.rating = fix_num(self.rating)

        self.weekly_hours = self.weekly_hours.replace('hours = ','').replace('"""','').split(';')

        
        for i in range(len(self.weekly_hours)):
            self.weekly_hours[i] = self.weekly_hours[i][4:].strip()

            if "/" in self.weekly_hours[i]:
                self.weekly_hours[i] = self.weekly_hours[i].split('/')

        fix_stu = lambda x : True if x == "yes" else False
        self.stu_discount = fix_stu(self.stu_discount)
        self.google_map = self.google_map.replace(',','')

    

class SearchService:
    def searchRestaurants(self, criteria):
        pass


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
        self.today_week = int(datetime.datetime.now().strftime("%w"))       #0=sunday
        self.today_week_t = datetime.datetime.now().strftime("%A")
        self.now_time = datetime.datetime.now().time()
        print(self.today_week,self.today_week_t,self.now_time)

    def restaurant_opening_hours_checking(self,x):

        try:
            if self.hours[self.today_week] =="closed":
                pass
            else:
                a = x.replace('–', '-').split('-')
                opening_hour = datetime.datetime.strptime(a[0].strip(),"%H:%M").time()
                closing_hour = datetime.datetime.strptime(a[1].strip(),"%H:%M").time()
                today_date = datetime.datetime.now().date()
                closing_datetime = datetime.datetime.combine(today_date, closing_hour)
                last_time = (closing_datetime - datetime.timedelta(minutes=30)).time()
                print(today_date,closing_datetime,last_time)
                print(opening_hour,closing_hour)

                if opening_hour <= self.now_time <= closing_hour:
                    if self.now_time >= last_time:
                        print("near last order / closing")
                    return True
                else:
                    return False    #closed
        except Exception as e:
            return False

    def restaurant_opening_hours(self):
        if isinstance(self.hours[self.today_week], list):
            for shift in self.hours[self.today_week]:
                if self.restaurant_opening_hours_checking(shift):
                    return True
            return False
        else:
            return self.restaurant_opening_hours_checking(self.hours[self.today_week])


class Restaurant:
# id,name,location,lat,lon,cuisines,price_level,dietary_tags,rating,weekly_hours,stu_discount,phone,website,google_map

    def __init__(self, id, name, location, lat, lon, cuisines, price_level, dietary_tags, rating, weekly_hours, stu_discount, phone, website, google_map):
        self.id = id
        self.name = name
        self.location = location
        self.lat = lat
        self.lon = lon        
        self.cuisines = cuisines
        self.price_level = price_level
        self.dietary_tags = dietary_tags
        self.rating = rating
        self.weekly_hours = weekly_hours
        self.stu_discount = stu_discount
        self.phone = phone
        self.website = website
        self.google_map = google_map



test = CsvRestaurantRepository()
print("hi")
test.read_file()

test2 = WeeklyHours(test.restaurant_list[0])        #"Top Blade Steak Lab"
test2.today_time()
print(test2.restaurant_opening_hours())
