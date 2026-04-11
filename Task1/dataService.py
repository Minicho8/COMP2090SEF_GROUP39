import os, csv, math
from datetime import datetime
from models import Campus,Location

# Restaurant Object 
class Restaurant:
# id,name,address,lat,lon,cuisines,price_level,dietary_tags,rating,hours,stu_discount,phone,wesite1,website, ,google_map
    def __init__(self, id=None, name=None, location=None, address=None, type=None, price_level=None, rating=None, dietary_tags=None, weekly_hours=None, stu_discount=None, phone=None, website=None, google_map=None):
        self.id = id
        self.name = name
        self.address = address
        self.location = location
        self.type = type
        self.price_level = price_level
        self.rating = rating
        self.dietary_tags = dietary_tags
        self.weekly_hours = weekly_hours
        self.stu_discount = stu_discount
        self.phone = phone
        self.website = website
        self.google_map = google_map

# Function for Reading the CSV File that contains the Restaurant info
class CsvRestaurantRepository:
    
    #Inner Class for use in Linked Objects
    class Node:
        def __init__(self, restaurant_obj):
            self.restaurant = restaurant_obj
            self.next = None

    # Initial Prepare for read file (check path)
    def __init__(self, file_path=None):
        self.head = None
        self.tail = None

        if file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.file_path = os.path.join(base_dir, 'restaurants.csv')
        else:
            self.file_path = file_path

    # add restaurant data to the tail of the linked object    
    def add_restaurant(self, restaurant_obj):
        new_node = self.Node(restaurant_obj)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    # function to format the row and make it suitable for further use
    def _parse_row(self, row):
        id = int(row[0])
        name = row[1]
        address = row[2]
        lat = float(row[3]) if row[3] else 0.0
        lon = float(row[4]) if row[4] else 0.0
        location = Location(lat,lon)
        type = row[5]
        dietary_tags = row[7].split(',')
        price_level = 0 if row[6] == '/' else int(row[6])
        rating = 0 if row[8] == '/' else int(row[8])
        weekly_hours = row[9]
        stu_discount = row[10]
        phone = row[11]
        website = row[12]

        obj_weekly_hours = self._parse_hours(weekly_hours)

        return Restaurant(
            id = id, 
            name = name, 
            address = address, 
            location = location, 
            type = type, 
            price_level = price_level, 
            rating = rating, 
            dietary_tags = dietary_tags, 
            weekly_hours = obj_weekly_hours, 
            stu_discount = stu_discount, 
            phone = phone, 
            website = website
        )
    
    # convert the opening hour data to a object (store the opening hours data in a more accessable way)
    @staticmethod
    def _parse_hours(data):
        hours_str = data
        hours_obj = {}
        
        hours_str = hours_str.replace('–', '-')
        cleaned_str = hours_str.replace("hours = ", "").strip('"')
        days = cleaned_str.split(';')
        for day_range in days:
            day, times = day_range.split('=')
            day = day.strip()
            times = times.strip()

            if times.lower() == 'closed':
                hours_obj[day] = []
            else:
                range_list = []
                for r in times.split('/'):
                    start, end = r.split('-')
                    #print(start.strip(), end.strip())
                    range_list.append((
                        datetime.strptime(start.strip(), "%H:%M").time(),
                        datetime.strptime(end.strip(), "%H:%M").time()
                    ))
                hours_obj[day] = range_list
        return hours_obj
    
    def read_file(self):            
        with open(self.file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if not row or not row[0].isdigit():
                    continue
                restaurant_obj = self._parse_row(row)
                self.add_restaurant(restaurant_obj)
    
    def get_all_restaurants(self):
        current = self.head
        while current:
            yield current.restaurant
            current = current.next

class SearchService:
    def __init__(self, repo):
        self._repo = repo

    def execute_search(self, criteria):
        self.search_criteria = criteria
        c = criteria
        results = []

        for restaurant in self._repo.get_all_restaurants():

            if c.query is not None and not c.query == "":
                if not(c.query in restaurant.name.lower()): 
                    continue
            if c.max_d is not None:
                if not(c.max_d >= (math.ceil(round(restaurant.location.distance_km_from(Campus().get_campus(c.campus))*100)/10)/10)):
                    continue
            if c.type is not None:
                if not(restaurant.type == c.type):
                    continue
            if c.max_p is not None:
                if not(int(c.max_p) >= int(restaurant.price_level)):
                    continue
            if c.min_rating is not None:
                if not((c.min_rating) <= (restaurant.rating)):
                    continue
            if c.dietary_tag is not None:
                if not(c.dietary_tag in restaurant.dietary_tags):
                    continue
            
            #"open_time": self.open_time,

            results.append(restaurant)
        return results
        #"sort": self.sort,
        #sort_restaurant(c.sort, self.search_criteria)
    #def sort_restaurant(self.)

    def get_field_val_list(self, field_name):            
        result_list = []
        for restaurant in self._repo.get_all_restaurants():
            if hasattr(restaurant, field_name):
                val = getattr(restaurant, field_name)
                if isinstance(val, list):
                    for i in val:
                        if i and i not in result_list:
                            result_list.append(i)
                elif val and val not in result_list:
                    result_list.append(val)
        return result_list
    
class SearchCriteria:
    def __init__(self):
        self.query = None # Keyword search query
        self.max_d = None # Maximum search distance in km (max_distance_km)
        self.type = None # Cuisine type (cuisine)
        self.max_p = None # Maximum price level (max_price_level)
        self.min_rating = None # Minimum rating (min_rating)
        self.dietary_tag = None # Dietary restriction tag (dietary_tag)
        self.open_time = None # Opening time filter (open_time)
        self.campus = None

    def update(self, query="NoInput", max_d="NoInput", type="NoInput", max_p="NoInput", min_rating="NoInput", dietary_tag="NoInput", open_time="NoInput", campus="NoInput"): 
        # Update the search criteria from user input variables
        if query != "NoInput": self.query = query
        if max_d != "NoInput": self.max_d = max_d
        if type != "NoInput": self.type = type
        if max_p != "NoInput": self.max_p = max_p
        if min_rating != "NoInput": self.min_rating = min_rating
        if dietary_tag != "NoInput": self.dietary_tag = dietary_tag
        if open_time != "NoInput": self.open_time = open_time
        if campus != "NoInput": self.campus = campus

        