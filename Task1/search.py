
class SearchCriteria:
    def __init__(self):
        self.query = None # Keyword search query
        self.max_d = None # Maximum search distance in km (max_distance_km)
        self.cuisine = None # Cuisine type (cuisine)
        self.max_p = None # Maximum price level (max_price_level)
        self.min_rating = None # Minimum rating (min_rating)
        self.dietary_tag = None # Dietary restriction tag (dietary_tag)
        self.open_time = None # Opening time filter (open_time)
        self.campus = None

    def update(self, query=None, max_d=None, cuisine=None, max_p=None, min_rating=None, dietary_tag=None, open_time=None, campus=None): 
        # Update the search criteria from user input variables
        if query is not None: self.query = query
        if max_d is not None: self.max_d = max_d
        if cuisine is not None: self.cuisine = cuisine
        if max_p is not None: self.max_p = max_p
        if min_rating is not None: self.min_rating = min_rating
        if dietary_tag is not None: self.dietary_tag = dietary_tag
        if open_time is not None: self.open_time = open_time
        if campus is not None: self.campus = campus

    def get_all(self):
        return {
            "query": self.query,
            "max_d": self.max_d,
            "cuisine": self.cuisine,
            "max_p": self.max_p,
            "min_rating": self.min_rating,
            "dietary_tag": self.dietary_tag,
            "open_time": self.open_time,
            "campus": self.campus
        }
class SearchResult:
    def __init__(self, title, url):
        self.title = title
        self.url = url

