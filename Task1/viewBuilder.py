import os
import math
import webbrowser
import tkinter as tk
import tkintermapview
from PIL import Image, ImageTk
from location import Campus, EstimatedWalkingtime
from data import WeeklyHours as w
from search import Search, Criteria

c = Campus()

class HomeView(tk.Frame):
    def __init__(self, parent, repo, nav_main, criteria):
        super().__init__(parent)
        self.search_service = Search(repo)
        self.nav_main = nav_main
        self._build_ui()
        if criteria is None or criteria.campus is None:
            self.criteria = Criteria()
        else:
            self.criteria = criteria
            self._change_background(self.criteria.campus)
            self.show_search_criteria()
            
        

    def _build_ui(self):
        bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "background.png")
        self.original_bg_image = Image.open(bg_path)
        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.bind("<Configure>", self._resize_image)

        # Center overlay card frame to make UI stand out from map
        self.card_frame = tk.Frame(self, bg="#ffffff", bd=0, highlightbackground="#cccccc", highlightthickness=1)
        self.card_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(self.card_frame, text="Welcome to Restaurant Search", font=("Segoe UI", 24, "bold"), fg="#333333", bg="#ffffff")
        title_label.pack(pady=(40, 30), padx=40)

        # Campus selection section (shown first)
        self.campus_selection_frame = tk.Frame(self.card_frame, bg="#ffffff")
        self.campus_selection_frame.pack(pady=(0, 40), padx=40)
        
        tk.Label(self.campus_selection_frame, text="Select your current campus location:", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").pack(pady=(0, 10))
        
        self.campus_var = tk.StringVar(value="Select Campus")
        campus_options = ["MC", "IOH", "JCC", "HMT_PLAZA"]
        
        # Style the dropdown slightly
        dropdown = tk.OptionMenu(self.campus_selection_frame, self.campus_var, *campus_options)
        dropdown.config(font=("Segoe UI", 11), bg="#f9f9f9", width=20, bd=1, relief="solid", activebackground="#eeeeee")
        dropdown.pack(pady=(0, 20))
        
        

        btn_confirm_campus = tk.Button(self.campus_selection_frame, text="Confirm", font=("Segoe UI", 12, "bold"), bg="#27ae60", fg="white", activebackground="#219150", activeforeground="white", bd=0, cursor="hand2", width=15, command=self._confirm_campus)
        btn_confirm_campus.pack()
        
        # Primary navigation buttons (created but NOT packed yet)
        self.btn_search = tk.Button(self.card_frame, text="Search for Restaurants", font=("Segoe UI", 13, "bold"), width=25, height=2, bg="#0066cc", fg="white", activebackground="#004080", activeforeground="white", bd=0, cursor="hand2", command=self.show_search_criteria)
        self.btn_all = tk.Button(self.card_frame, text="Show All Restaurants", font=("Segoe UI", 13, "bold"), width=25, height=2, bg="#f39c12", fg="white", activebackground="#e67e22", activeforeground="white", bd=0, cursor="hand2", command=lambda: self.nav_main(self.criteria))
        
        # Back button to return to campus selection
        self.btn_back_to_campus = tk.Button(self.card_frame, text="⬅ Back to Campus Selection", font=("Segoe UI", 11), bg="#ffffff", fg="#c0392b", activebackground="#f9f9f9", activeforeground="#a53125", bd=0, cursor="hand2", command=self.back_to_campus)

    def _confirm_campus(self):
        if self.campus_var.get() and self.campus_var.get() != "Select Campus":
            # Update the instance created in __init__
            self.criteria.update(campus=self.campus_var.get())
            campus_val = self.criteria.campus

            print(campus_val)
            
            self._change_background(campus_val)
            
            # Hide the selection section
            self.campus_selection_frame.pack_forget()
            # Show the primary navigation buttons
            self.btn_search.pack(pady=(0, 15), padx=40)
            self.btn_all.pack(pady=(0, 15), padx=40)
            self.btn_back_to_campus.pack(pady=(0, 40), padx=40)
    
    def _change_background(self, campus_name):
        bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"background{campus_name}.png")
        try:
            self.original_bg_image = Image.open(bg_path)
            # Force a resize event to apply the new image immediately
            e = tk.Event()
            e.widget = self
            e.width = self.winfo_width()
            e.height = self.winfo_height()
            self._resize_image(e) 
        except Exception as e:
            pass

    def back_to_campus(self):
        # Hide primary buttons
        self.btn_search.pack_forget()
        self.btn_all.pack_forget()
        self.btn_back_to_campus.pack_forget()

        # Reset background back to original default
        bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "background.png")
        try:
            self.original_bg_image = Image.open(bg_path)
            e = tk.Event()
            e.widget = self
            e.width = self.winfo_width()
            e.height = self.winfo_height()
            self._resize_image(e) 
        except Exception as e:
            pass

        # Show campus selection panel again
        self.campus_selection_frame.pack(pady=(0, 40), padx=40)

    def _resize_image(self, event):
        # We only want to resize if the container frame itself triggered the event
        if event.widget == self and event.width > 50 and event.height > 50:
            resized_image = self.original_bg_image.resize((event.width, event.height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_image)
            self.bg_label.config(image=self.bg_image)

    def show_search_criteria(self):
        self.campus_selection_frame.pack_forget()
        self.btn_search.pack_forget()
        self.btn_all.pack_forget()
        self.btn_back_to_campus.pack_forget()

        self.criteria_frame = tk.Frame(self.card_frame, bg="#ffffff")
        self.criteria_frame.pack(pady=(0, 40), padx=40)

        tk.Label(self.criteria_frame, text="Restaurant Name (Optional):", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        query_var = tk.StringVar()
        tk.Entry(self.criteria_frame, textvariable=query_var, font=("Segoe UI", 12), bg="#f9f9f9", relief="solid", bd=1, width=17).grid(row=0, column=1, padx=10, pady=10,sticky="w")

        tk.Label(self.criteria_frame, text="Max Distance:", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        max_d_var = tk.StringVar()
        max_d_frame = tk.Frame(self.criteria_frame, bg="#ffffff")
        max_d_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        max_d_selectors = [(0.3, "300m"), (0.5, "500m"), (1, "1km"), (1.5, "1.5km"), (2, "2km"), ("any", "Any")]
        for valD, text in max_d_selectors:
            tk.Radiobutton(max_d_frame, text=text, variable=max_d_var, value=valD, indicatoron=0, bg="#f9f9f9", selectcolor="#d0e8f1", font=("Segoe UI", 10), width=5).pack(side=tk.LEFT, padx=2)

        tk.Label(self.criteria_frame, text="Cuisine/ Restaurant Type:", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        type_var = tk.StringVar()
        type_selectors = self.search_service.get_field_val_list("type")
        
        type_menu = tk.OptionMenu(self.criteria_frame, type_var, "Any Type",*type_selectors)
        type_menu.config(font=("Segoe UI", 12), bg="#f9f9f9", relief="solid", bd=0, width=17)
        type_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.criteria_frame, text="Price Range:", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        price_var = tk.StringVar()
        price_frame = tk.Frame(self.criteria_frame, bg="#ffffff")
        price_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        price_selectors = [(1, "<$50"), (2, "<$100"), (3, "<$200"), (4, "Any Price")]
        for valP, text in price_selectors:
            tk.Radiobutton(price_frame, text=text, variable=price_var, value=valP, indicatoron=0, bg="#f9f9f9", selectcolor="#d0e8f1", font=("Segoe UI", 10), width=9).pack(side=tk.LEFT, padx=2)

        # Rating input
        tk.Label(self.criteria_frame, text="★ Rating:", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        
        rating_var = tk.StringVar()
        rating_selectors = ["★+", "★★+", "★★★+", "★★★★+", "★★★★★"]

        rating_menu = tk.OptionMenu(self.criteria_frame, rating_var, "Any Rating", *rating_selectors)
        rating_menu.config(font=("Segoe UI", 12), bg="#f9f9f9", relief="solid", bd=0, width=17)
        rating_menu.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.criteria_frame, text="Dietary Tag:", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        dietary_var = tk.StringVar()
        dietary_selectors = self.search_service.get_field_val_list("dietary_tags")
        
        dietary_menu = tk.OptionMenu(self.criteria_frame, dietary_var, "(Optional)",*dietary_selectors)
        dietary_menu.config(font=("Segoe UI", 12), bg="#f9f9f9", relief="solid", bd=0, width=17)
        dietary_menu.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.criteria_frame, text="Currently Open:", font=("Segoe UI", 12), bg="#ffffff", fg="#333333").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        time_var = tk.StringVar(value="")
        tk.Checkbutton(self.criteria_frame, text="Yes", variable=time_var, onvalue="now", offvalue="", bg="#ffffff", font=("Segoe UI", 12)).grid(row=6, column=1, padx=10, pady=10, sticky="w")

        def fix_search():
            fix_query = query_var.get() if query_var.get() else None

            fix_max_d = float(max_d_var.get()) if max_d_var.get() and not(max_d_var.get() == "any") else None
            if max_d_var.get() == "any": fix_max_d = None

            if type_var.get():
                if type_var.get() == "Any Type": fix_type = None
                else: fix_type = type_var.get()

            fix_price = price_var.get() if price_var.get() else  None
            if price_var.get() == "4": fix_price = None

            if rating_var.get():
                if rating_var.get() == "Any Rating": fix_rating = None
                elif rating_var.get() == "★+": fix_rating = 1
                elif rating_var.get() == "★★+": fix_rating = 2
                elif rating_var.get() == "★★★+": fix_rating = 3
                elif rating_var.get() == "★★★★+": fix_rating = 4
                elif rating_var.get() == "★★★★★": fix_rating = 5
                else: fix_rating = None

            if dietary_var.get():
                if dietary_var.get() == "(Optional)": fix_dietary_tag = None
                else: fix_dietary_tag = dietary_var.get()

            fix_otime = time_var.get() if time_var.get() else None  
            self.criteria.update(
                query = fix_query,
                max_d = fix_max_d,
                type = fix_type,
                max_p = fix_price,
                min_rating = fix_rating,
                dietary_tag = fix_dietary_tag,
                open_time = fix_otime
            )
            
            #print(self.criteria)
            self.nav_main(self.criteria)

        def reset():
            query_var.set("")
            max_d_var.set("any")
            type_var.set("Any Type")
            price_var.set(4)
            rating_var.set("Any Rating") 
            dietary_var.set("(Optional)")
            time_var.set("")

        def back():
            if self.criteria is not None:
                self.nav_main(self.criteria)
            else:
                self.criteria_frame.destroy()

                self.btn_search.pack(pady=(0, 15), padx=40)
                self.btn_all.pack(pady=(0, 15), padx=40)
                self.btn_back_to_campus.pack(pady=(0, 40), padx=40)
        btn_frame = tk.Frame(self.criteria_frame, bg="#ffffff")
        btn_frame.grid(row=7, column=0, columnspan=2, pady=(20, 10))

        tk.Button(btn_frame, text="Start Search", bg="#27ae60", fg="white", activebackground="#219150", activeforeground="white", bd=0, cursor="hand2", font=("Segoe UI", 12, "bold"), width=15, command=fix_search).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reset", bg="#f39c12", fg="white", activebackground="#e67e22", activeforeground="white", bd=0, cursor="hand2", font=("Segoe UI", 12, "bold"), width=10, command=reset).pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.criteria_frame, text="Cancel", bg="#c0392b", fg="white", activebackground="#a53125", activeforeground="white", bd=0, cursor="hand2", font=("Segoe UI", 11), width=10, command=back).grid(row=8, column=0, columnspan=2)

        reset()

    
class MainView(tk.Frame):
    def __init__(self, parent, repo, nav_home, criteria=None):
        super().__init__(parent)
        self.search_service = Search(repo)
        self.nav_home = nav_home
        self.criteria = criteria
        self.displayed_restaurants = []
        self.current_google_map_url = ""

        self.search_var = tk.StringVar()
        self.dropdown_var = tk.StringVar(value="Settings")

        self._build_ui()
        
    def _build_ui(self):
        # Add a top label (Header) with left button and right dropdown
        header_frame = tk.Frame(self)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        left_btn = tk.Button(header_frame, text="Advance Search", command=lambda: self.nav_home(self.criteria), bg="#2196F3", fg="white")
        left_btn.pack(side=tk.LEFT)

        title = tk.Label(header_frame, text="Restaurant Search Suggestion System", font=("Helvetica", 18, "bold"))
        title.pack(side=tk.LEFT, expand=True)
        def change_campus():
            self.criteria.update(campus=None) 
            self.nav_home(self.criteria)
        right_btn = tk.Button(header_frame, text="Change Campus", command=change_campus, bg="#2196F3", fg="white")
        right_btn.pack(side=tk.RIGHT)

        # Create two side-by-side frames
        content_frame = tk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Configure columns to have equal width by using the same "uniform" group
        content_frame.columnconfigure(0, weight=1,uniform='half')
        content_frame.columnconfigure(1, weight=1,uniform='half')
        content_frame.rowconfigure(0, weight=1)

        left_frame = tk.Frame(content_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right_frame = tk.Frame(content_frame)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Results Listbox
        results_frame = tk.Frame(left_frame, bg="#ffffff", bd=1, relief="solid")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Header for the listbox
        list_header_frame = tk.Frame(results_frame, bg="#f1f1f1")
        list_header_frame.pack(fill=tk.X)
        tk.Label(list_header_frame, text="Search Results", font=("Segoe UI", 11, "bold"), bg="#f1f1f1", fg="#333333").pack(side=tk.LEFT, padx=10, pady=8)

        scrollbar = tk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            results_frame, 
            yscrollcommand=scrollbar.set, 
            font=("Segoe UI", 12),
            bg="#ffffff",
            fg="#333333",
            selectbackground="#0066cc",
            selectforeground="#ffffff",
            activestyle="none", # removes the dotted line around the selected item
            highlightthickness=0,
            bd=0,
            relief="flat"
        )

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar.config(command=self.listbox.yview)

        # TkinterMapView and Info Card on the right frame
        info_frame = tk.Frame(right_frame, bg="#ffffff", bd=1, relief="solid")
        info_frame.pack(fill=tk.X, pady=(0, 10))

        info_header_frame = tk.Frame(info_frame, bg="#f1f1f1")
        info_header_frame.pack(fill=tk.X)

        tk.Label(info_header_frame, text="Restaurant Details", font=("Segoe UI", 12, "bold"), bg="#f1f1f1", fg="#333333").pack(side=tk.LEFT, padx=10, pady=8)
        
        deselect_btn = tk.Button(info_header_frame, text="✖ Deselect", command=self.cancel_selection, bg="#e0e0e0", activebackground="#cccccc", relief="flat", bd=0, cursor="hand2", padx=8, pady=2)
        deselect_btn.pack(side=tk.RIGHT, padx=10, pady=8)

        # Better detailed layout
        self.details_frame = tk.Frame(info_frame, bg="#ffffff")
        self.details_frame.pack(fill=tk.BOTH, padx=15, pady=10)
        
        # Title line framework
        self.title_line_frame = tk.Frame(self.details_frame, bg="#ffffff")
        self.title_line_frame.pack(fill=tk.X, pady=(0, 2))

        # Name
        self.lbl_r_name = tk.Label(self.title_line_frame, text="Select a restaurant from the list to view its information.", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#0066cc", anchor="w")
        self.lbl_r_name.pack(side=tk.LEFT)

        # Open Status
        self.lbl_open_status = tk.Label(self.title_line_frame, text="", font=("Segoe UI", 9, "bold"), padx=5, pady=2)
        # Hidden by default until a restaurant is selected
        
        # Distance and Walking Time
        self.lbl_r_dist = tk.Label(self.details_frame, text="", font=("Segoe UI", 9, "italic"), bg="#ffffff", fg="#888888", anchor="w", justify="left")
        self.lbl_r_dist.pack(fill=tk.X, pady=(2, 0))

        # Horizontal layout for stats (Type badge, Price, Rating, Tags)
        self.stats_frame = tk.Frame(self.details_frame, bg="#ffffff")
        self.stats_frame.pack(fill=tk.X, pady=(10, 5))
        
        # Badge style for cuisine
        self.lbl_r_type = tk.Label(self.stats_frame, text="", font=("Segoe UI", 10, "bold"), bg="#e1f5fe", fg="#0066cc", padx=8, pady=2)
        
        # Price and Rating
        self.lbl_r_price = tk.Label(self.stats_frame, text="", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#27ae60")
        self.lbl_r_rating = tk.Label(self.stats_frame, text="", font=("Segoe UI", 11), bg="#ffffff", fg="#f39c12")
        
        # Dietary tags
        self.diet_tags_frame = tk.Frame(self.stats_frame, bg="#ffffff")
        #self.lbl_r_diet = tk.Label(self.stats_frame, text="", font=("Segoe UI", 9), bg="#f5f5f5", fg="#666666", padx=5, pady=2) # Keep fallback if needed, but we will mostly use diet_tags_frame

        # Address
        self.address_frame = tk.Frame(self.details_frame, bg="#ffffff")

        lbl_addr_title = tk.Label(self.address_frame, text="Address:", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#333333", anchor="nw")
        lbl_addr_title.grid(row=0, column=0, sticky="nw", padx=(0, 10))

        self.lbl_r_addr = tk.Label(self.address_frame, text="", font=("Consolas", 10), bg="#ffffff", fg="#000000", anchor="nw", justify=tk.LEFT, wraplength=350)
        self.lbl_r_addr.grid(row=0, column=1, sticky="nw")

        # Hours area (Using a frame to align title and time text nicely)
        self.hours_frame = tk.Frame(self.details_frame, bg="#ffffff")
        
        lbl_hours_title = tk.Label(self.hours_frame, text="Opening Hours:", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#333333", anchor="nw")
        lbl_hours_title.grid(row=0, column=0, sticky="nw", padx=(0, 10))
        
        self.lbl_r_hours = tk.Label(self.hours_frame, text="", font=("Consolas", 10), bg="#ffffff", fg="#444444", anchor="nw", justify=tk.LEFT)
        self.lbl_r_hours.grid(row=0, column=1, sticky="nw")

        self.map_widget = tkintermapview.TkinterMapView(right_frame, width=400, height=400, corner_radius=0)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.pack(fill=tk.BOTH, expand=True)

        # Default to HKMU Ho Man Tin Campuses, adjust zoom
        o_lat = c.get_campus("MC").lat + c.get_campus("IOH").lat + c.get_campus("JCC").lat + c.get_campus("HMT_PLAZA").lat
        o_lon = c.get_campus("MC").lon + c.get_campus("IOH").lon + c.get_campus("JCC").lon + c.get_campus("HMT_PLAZA").lon
        self.map_widget.set_position(o_lat / 4, o_lon / 4)
        self.map_widget.set_zoom(17)

        # Create Reload Button and place it hovering on the top right
        reload_btn = tk.Button(self.map_widget, text="↻ Reload Map", command=self.reload_map, bg="white", activebackground="#f0f0f0", relief=tk.RAISED, bd=1)
        reload_btn.place(relx=1.0, anchor=tk.NE, x=-10, y=10)

        # Navigation Button for Google Maps (Hidden by default until a restaurant is selected)
        self.btn_nav_google = tk.Button(self.map_widget, text="Navigate in Google Maps", bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white", font=("Segoe UI", 11, "bold"), relief="flat", bd=0, cursor="hand2")
                
        self.btn_nav_google.config(command=self.open_google_maps)

        self.listbox.bind("<<ListboxSelect>>", self.on_restaurant_select)
        self.listbox.bind("<Up>", self.block_event)
        self.listbox.bind("<Down>", self.block_event)

        
        # Populate the list initially
        self.perform_search()

    def open_google_maps(self):
        if self.current_google_map_url:
            webbrowser.open(self.current_google_map_url)

    def cancel_selection(self):
        self.listbox.selection_clear(0, tk.END)
        self.reload_map()
        
        # Reset labels
        self.lbl_r_name.config(text="Select a restaurant from the list to view its information.")
        self.lbl_open_status.pack_forget()
        self.lbl_r_addr.config(text="")
        self.current_google_map_url = ""
        
        # Hide dynamic blocks
        self.lbl_r_type.pack_forget()
        self.lbl_r_price.pack_forget()
        self.lbl_r_rating.pack_forget()
        self.lbl_r_diet.pack_forget()        
        self.diet_tags_frame.pack_forget()        
        self.hours_frame.pack_forget()
        self.btn_nav_google.place_forget()

    # Reload Map Function
    def reload_map(self):
        selected_indices = self.listbox.curselection()
        if selected_indices and selected_indices[0] < len(self.displayed_restaurants):
            # A restaurant is currently selected, center map on it instead of resetting everything
            r = self.displayed_restaurants[selected_indices[0]]
            self.map_widget.delete_all_marker()
            self.map_widget.set_position(r.location.lat, r.location.lon)
            self.map_widget.set_zoom(17)
            self.map_widget.set_marker(r.location.lat, r.location.lon, text=r.name)
        else:
            # No restaurant selected, do a full map reset to default coordinates
            self.map_widget.delete_all_marker()
            o_lat = c.get_campus("MC").lat + c.get_campus("IOH").lat + c.get_campus("JCC").lat + c.get_campus("HMT_PLAZA").lat
            o_lon = c.get_campus("MC").lon + c.get_campus("IOH").lon + c.get_campus("JCC").lon + c.get_campus("HMT_PLAZA").lon
            print(o_lat, o_lon)
            self.map_widget.set_position(o_lat / 4, o_lon / 4)
            self.map_widget.set_zoom(17)

    # Define the search function
    def perform_search(self):
        self.listbox.delete(0, tk.END)
        self.displayed_restaurants.clear()
        results_found = False
        
        for idx, r in enumerate(self.search_service.execute_search(self.criteria)):
            print('idx:',idx)
            # Add dynamic visual indicators like emoji or clean formatting
            rating_str = '★' * int(r.rating) if r.rating else 'No Rating'
            display_text = f" 🍽️ {r.name}  | {r.type.upper()} {rating_str}"
            print("~"*10)
            self.listbox.insert(tk.END, display_text)
            
            # Alternate row colors for better readability
            bg_color = "#ffffff" if idx % 2 == 0 else "#f9f9f9"
            self.listbox.itemconfig(tk.END, {'bg': bg_color})
            
            self.displayed_restaurants.append(r)
            results_found = True
                
        if not results_found:
            self.listbox.insert(tk.END, "  🔍 No matching restaurants found for your query.")
            self.listbox.itemconfig(tk.END, {'fg': '#888888'})
    def on_restaurant_select(self,event):
        # Find which item is clicked
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            return
        index = selected_indices[0]
        # Make sure don't crash if they click the "No matching..." text
        if index < len(self.displayed_restaurants):
            r = self.displayed_restaurants[index]
            lat = r.location.lat
            lon = r.location.lon
            # Place map marker
            self.map_widget.delete_all_marker()
            self.map_widget.set_position(lat, lon)
            self.map_widget.set_zoom(17)
            self.map_widget.set_marker(lat, lon, text=r.name)
            # Update info card with structured layout
            self.lbl_r_name.config(text=r.name)
            
            # Check Open Status
            nt = w()
            if Search.is_open(r.weekly_hours,nt.today_week,nt.now_time):
                self.lbl_open_status.config(text="OPEN NOW", bg="#d4edda", fg="#27ae60")
            else:
                self.lbl_open_status.config(text="CLOSED", bg="#f8d7da", fg="#dc3545")
            self.lbl_open_status.pack(side=tk.LEFT, padx=(10, 0))

            # Distance and Walk Time calculation
            campus_loc = c.get_campus(self.criteria.campus)
            dist_km = r.location.distance_km_from(campus_loc)
            
            print(self.criteria.campus,dist_km)
            print("~"*10)
            if dist_km >= 1:
                dist_text = (str(round(dist_km,2)) + " km") 
            elif dist_km < 0.1:
                dist_text = "< 100 m"
            elif dist_km <0.2:
                dist_text = (str(round(dist_km*100)*10)+ " m")
            else:
                dist_text = (str(math.ceil(round(dist_km*100)/10)*100)+ " m")
            walk_time = EstimatedWalkingtime().estimated_walking_time(dist_km)
            self.lbl_r_dist.config(text=f"📌 Distance: {dist_text}  •  🚶 Est. Walk: {walk_time} min")
            
            # Generate visual strings
            price_str = int(r.price_level) * '$' + (4 - int(r.price_level)) * '  '
            self.lbl_r_price.config(text=price_str)
            self.lbl_r_price.pack(side=tk.LEFT, padx=(0, 15))

            rating_str = int(r.rating) * '★ ' + (5 - int(r.rating)) * '☆ '
            self.lbl_r_rating.config(text=rating_str)
            self.lbl_r_rating.pack(side=tk.LEFT, padx=(0, 15))
            
            #
            if r.type and r.type != '/':
                self.lbl_r_type.config(text=r.type.upper())
            else:
                self.lbl_r_type.config(text="RESTURANT")
            self.lbl_r_type.pack(side=tk.LEFT, padx=(0, 15))

            #
            if r.dietary_tags and r.dietary_tags != ['']:
                print(r.dietary_tags)
                self.diet_tags_frame.pack(side=tk.LEFT, padx=(5, 0))
                for label in self.diet_tags_frame.winfo_children():
                    label.destroy()
                for tag in r.dietary_tags:
                    tag = tag.strip()
                    if tag and tag != '':
                        tk.Label(self.diet_tags_frame, text=tag, font=("Segoe UI", 9), bg="#f5f5f5", fg="#666666", padx=5, pady=2).pack(side=tk.LEFT, padx=3)
            else:
                self.diet_tags_frame.pack_forget()

            # Show address
            self.lbl_r_addr.config(text=r.address)
            self.address_frame.pack(fill=tk.X, pady=(10, 0))

            # Show hours
            self.lbl_r_hours.config(text=w.textformat(r.weekly_hours))
            self.hours_frame.pack(fill=tk.X, pady=(10, 0))

            
            self.current_google_map_url = f"https://www.google.com/maps/dir/?api=1&origin={c.get_campus(self.criteria.campus).lat},{c.get_campus(self.criteria.campus).lon}&destination={lat},{lon}&travelmode=walking"

            # Reveal the interactive "Navigate in Google Maps" button embedded securely onto the map overlay
            self.btn_nav_google.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20, width=220, height=40)
    
    def block_event(self, event):
        return "break"