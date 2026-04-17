import os
import csv
from datetime import datetime
from location import Location

# Restaurant Object 
class Restaurant:
    def __init__(self, name=None, location=None, address=None, type=None, price_level=None, rating=None, dietary_tags=None, weekly_hours=None, stu_discount=None):
        self.name = name
        self.address = address
        self.location = location
        self.type = type
        self.price_level = price_level
        self.rating = rating
        self.dietary_tags = dietary_tags
        self.weekly_hours = weekly_hours
        self.stu_discount = stu_discount

# Function for Reading the CSV File
class Data:
    #Inner Class for use in Linked Objects
    class Node:
        def __init__(self, restaurant_obj):
            self.restaurant = restaurant_obj
            self.next = None

    def __init__(self, file_path=None):
        self.head = None
        self.tail = None

        if file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.file_path = os.path.join(base_dir, 'restaurantv3.csv')
        else:
            self.file_path = file_path

    # add restaurant data to the tail of the linked object   
    def __add_restaurant(self, restaurant_obj):
        new_node = self.Node(restaurant_obj)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    # function to format the row and make it suitable for further use
    def __parse_row(self, row):
        name = row[0]
        address = row[1]
        lat = float(row[2]) if row[2] else 0.0
        lon = float(row[3]) if row[3] else 0.0
        location = Location(lat,lon)
        type = row[4]
        dietary_tags = row[6].split(',')
        price_level = 0 if row[5] == '' else int(row[5])
        rating = 0 if row[7] == '/' else int(row[7])
        weekly_hours = row[8]
        stu_discount = row[9]

        obj_weekly_hours = WeeklyHours.parse_hours(weekly_hours)

        return Restaurant(
            name = name, 
            address = address, 
            location = location, 
            type = type, 
            price_level = price_level, 
            rating = rating, 
            dietary_tags = dietary_tags, 
            weekly_hours = obj_weekly_hours, 
            stu_discount = stu_discount
        )
    
    def read_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if not row:
                    continue
                restaurant_obj = self.__parse_row(row)
                self.__add_restaurant(restaurant_obj)

    def get_all_restaurants(self):
        current = self.head
        while current:
            yield current.restaurant
            current = current.next

class WeeklyHours:
    def __init__(self):
        self.today_week = int(datetime.now().strftime("%w"))
        self.now_time = datetime.now().time()

    @staticmethod
    def parse_hours(data):
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
                for r in times.split(','):
                    start, end = r.split('-')
                    range_list.append((
                        datetime.strptime(start.strip(), "%H:%M").time(),
                        datetime.strptime(end.strip(), "%H:%M").time()
                    ))
                hours_obj[day] = range_list
        return hours_obj
    
    @staticmethod
    def textformat(schedule):
        formatted_output = []
        for day, intervals in schedule.items():
            # Capitalize the day
            day_name = day.capitalize()
            if not intervals:
                status = "Closed"
            else:
                # Join multiple time slots with a comma
                status = ", ".join([f"{start.strftime('%H:%M')}-{end.strftime('%H:%M')}" for start, end in intervals])
            formatted_output.append(f"{day_name}: {status}")
        return "\n".join(formatted_output)



        