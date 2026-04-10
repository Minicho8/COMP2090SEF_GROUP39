import os
import csv
import search 
from models import Restaurant as r, WeeklyHours as w,Location

class RestaurantNode:
    def __init__(self, restaurant_obj):
        self.restaurant = restaurant_obj
        self.next = None

class CsvRestaurantRepository():
# id,name,address,lat,lon,cuisines,price_level,dietary_tags,rating,hours,stu_discount,phone,wesite1,website, ,google_map

    def __init__(self):
        self.head = None
        self.tail = None

    def read_file(self):
        # Build an absolute path to the CSV file based on this script's location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, 'restaurants.csv')
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if not row or not row[0].isdigit(): # For skip empty lines
                    continue 
                
                id = int(row[0])
                name = row[1]
                address = row[2]
                lat = float(row[3]) if row[3] else 0.0
                lon = float(row[4]) if row[4] else 0.0
                location = Location(lat,lon)
                cuisines = row[5]
                dietary_tags = row[7]
                price_level = 0 if row[6] == '/' else row[6]
                rating = 0 if row[8] == '/' else row[8]
                weekly_hours = row[9]
                stu_discount = row[10]
                phone = row[11]
                website = row[12]
                google_map = row[13]

                print(row)
                print(weekly_hours)
                
                obj_weekly_hours = w.parse_hours(weekly_hours)

                restaurant_obj = r(id=id, name=name, address=address, location=location, cuisines=cuisines, price_level=price_level, rating=rating, dietary_tags=dietary_tags, weekly_hours=obj_weekly_hours, stu_discount=stu_discount, phone=phone, website=website, google_map=google_map)
                new_node = RestaurantNode(restaurant_obj)

                if not self.head:
                    self.head = new_node
                    self.tail = new_node
                else:
                    self.tail.next = new_node
                    self.tail = new_node

    def get_all_restaurants(self):
        current = self.head
        while current:
            yield current.restaurant
            current = current.next
    

class SearchService:
    def __init__(self):
        self.search_criteria = search.SearchCriteria()
    def searchRestaurants(self, criteria):
        self.search_criteria = criteria
        pass