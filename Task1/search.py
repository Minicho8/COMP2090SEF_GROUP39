import math
from datetime import datetime
from location import Campus
class Search:
    def __init__(self, repo):
        self._repo = repo
    def execute_search(self, criteria):
        c = criteria
        results = []

        # restaurant filtering
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
            if c.open_time is not None and c.open_time == 'now':
                today_week = int(datetime.now().strftime("%w"))
                now_time = datetime.now().time()
                if not(self.is_open(restaurant.weekly_hours,today_week,now_time)):
                    continue
            results.append(restaurant)

        #restaurant sorting
        if c.campus is not None:
            campus_loc = Campus().get_campus(c.campus)
            results.sort(key=lambda r: r.location.distance_km_from(campus_loc))
        return results
    
    @staticmethod
    def is_open(hours_obj,day_of_week,time):
        if isinstance(day_of_week, int):
            days_map = {0: "sun", 1: "mon", 2: "tue", 3: "wed", 4: "thu", 5: "fri", 6: "sat"}
            day = days_map.get(day_of_week, "")
        else:
            day = day_of_week.lower()   
        if day not in hours_obj or not hours_obj[day]:
            return False
        if isinstance(time, str):
            check_time = datetime.strptime(time, "%H:%M").time()
        else:
            check_time = time
        for start, end in hours_obj[day]:
            # Check if time is within the range
            if start <= check_time <= end:
                return True
        return False
    def get_field_val_list(self, field_name):            
        result_list = []
        for restaurant in self._repo.get_all_restaurants():
            if hasattr(restaurant, field_name):
                val = getattr(restaurant, field_name)
                if isinstance(val, list):
                    for i in val:
                        i = i.strip()
                        if i and i not in result_list:
                            result_list.append(i)
                elif val and val.strip() not in result_list:
                    result_list.append(val.strip())
        result_list.sort()
        return result_list

class Criteria:
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