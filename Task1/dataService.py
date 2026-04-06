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
            id = int(each.strip().split(',')[0])
            name = each.strip().split(',')[1]
            location = each.strip().split(',')[2]
            cuisines = each.strip().split(',')[5]
            price_level = each.strip().split(',')[7]
            rating = each.strip().split(',')[8]
            dietary_tags = each.strip().split(',')[6]
            weekly_hours = each.strip().split(',')[9]

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