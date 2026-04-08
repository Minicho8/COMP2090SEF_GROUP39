
class SearchCriteria:
    def __init__(self, query):
        self.query = query
        self.max_d = None # Maximum search distance in km (max_distance_km)
        self.cuisine = None # Cuisine type (cuisine)
        self.max_p = None # Maximum price level (max_price_level)
        self.min_rating = None # Minimum rating (min_rating)
        self.dietary_tag = None # Dietary restriction tag (dietary_tag)
        self.open_time = None # Opening time filter (open_time)
    def update(self): #get the search criteria from user input
        pass
        
class SearchResult:
    def __init__(self, title, url):
        self.title = title
        self.url = url

