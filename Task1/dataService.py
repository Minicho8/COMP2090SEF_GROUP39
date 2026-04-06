import search 
from models import Restaurant as r

class CsvRestaurantRepository():
# id,name,address,lat,lon,cuisines,price_level,dietary_tags,rating,hours,stu_discount,phone,wesite1,website, ,google_map

    def __init__(self):
        self.restaurant_list = []

    def read_file(self):
        file = open('restaurants.csv','r', encoding='utf-8')
        file_lines = file.readlines()
        file.close()
        for each in file_lines:
            x = each.strip().split(',')
            id = int(x[0])
            name = x[1]
            location = x[2]
            cuisines = x[5]
            price_level = x[7]
            rating = x[8]
            dietary_tags = x[6]
            weekly_hours = x[9]

            location = location.replace(';',',')

            weekly_hours = weekly_hours.replace('hours = ','').replace('"""','').split(';')

            
            for i in range(len(weekly_hours)):
                weekly_hours[i] = weekly_hours[i][4:]

                if "/" in weekly_hours[i]:
                    weekly_hours[i] = weekly_hours[i].split('/')


            restaurant_obj = r(id, name, location, cuisines, price_level, rating, dietary_tags, weekly_hours)

            self.restaurant_list.append(restaurant_obj)

    

class SearchService:
    def searchRestaurants(self, criteria):
        pass