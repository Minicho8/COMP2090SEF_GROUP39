from models import Campus,WeeklyHours as w

import tkinter as ts
import tkintermapview

c = Campus()


def build_main_view(root, repo):

    # Create the main container frame
    main_frame = ts.Frame(root, padx=20, pady=20)
    main_frame.pack(fill=ts.BOTH, expand=True)

    # Add a top label (Header) with left button and right dropdown
    header_frame = ts.Frame(main_frame)
    header_frame.pack(fill=ts.X, pady=(0, 20))

    left_btn = ts.Button(header_frame, text="Menu", bg="#2196F3", fg="white")
    left_btn.pack(side=ts.LEFT)

    lbl_title = ts.Label(header_frame, text="Restaurant Search Suggestion System", font=("Helvetica", 18, "bold"))
    lbl_title.pack(side=ts.LEFT, expand=True)

    dropdown_var = ts.StringVar(value="Settings")
    dropdown_menu = ts.OptionMenu(header_frame, dropdown_var, "Profile", "Preferences", "Logout")
    dropdown_menu.config(bg="#f1f1f1")
    dropdown_menu.pack(side=ts.RIGHT)

    # Create a PanedWindow or two side-by-side frames
    content_frame = ts.Frame(main_frame)
    content_frame.pack(fill=ts.BOTH, expand=True)

    left_frame = ts.Frame(content_frame)
    left_frame.pack(side=ts.LEFT, fill=ts.BOTH, expand=True, padx=(0, 10))

    right_frame = ts.Frame(content_frame)
    right_frame.pack(side=ts.RIGHT, fill=ts.BOTH, expand=True)

    # Search section
    search_frame = ts.Frame(left_frame)
    search_frame.pack(fill=ts.X)
    ts.Label(search_frame, text="Keyword:").pack(side=ts.LEFT, padx=(0,10))

    search_var = ts.StringVar()
    search_entry = ts.Entry(search_frame, textvariable=search_var, width=30)
    search_entry.pack(side=ts.LEFT, padx=(0,10))

    # Remaining views - Create a Results Listbox
    results_frame = ts.Frame(left_frame)
    results_frame.pack(fill=ts.BOTH, expand=True, pady=20)

    scrollbar = ts.Scrollbar(results_frame)
    scrollbar.pack(side=ts.RIGHT, fill=ts.Y)
    
    listbox = ts.Listbox(results_frame, yscrollcommand=scrollbar.set, font=("Helvetica", 11))
    listbox.pack(side=ts.LEFT, fill=ts.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    # TkinterMapView and Info Card on the right frame
    info_frame = ts.Frame(right_frame, bg="#e8e8e8", bd=2, relief=ts.GROOVE)
    info_frame.pack(fill=ts.X, pady=(0, 10))

    info_var = ts.StringVar()
    info_var.set("Select a restaurant from the list to view its information.")

    def cancel_selection():
        listbox.selection_clear(0, ts.END)
        reload_map()
        info_var.set("Select a restaurant from the list to view its information.")

    info_header_frame = ts.Frame(info_frame, bg="#e8e8e8")
    info_header_frame.pack(fill=ts.X, padx=5, pady=(5,0))

    ts.Label(info_header_frame, text="Restaurant Details", font=("Helvetica", 12, "bold"), bg="#e8e8e8").pack(side=ts.LEFT)
    
    deselect_btn = ts.Button(info_header_frame, text="✖ Deselect", command=cancel_selection, bg="white", activebackground="#f0f0f0", relief=ts.RAISED, bd=1)
    deselect_btn.pack(side=ts.RIGHT)

    info_label = ts.Label(info_frame, textvariable=info_var, justify=ts.LEFT, anchor=ts.W, font=("Helvetica", 10), bg="#e8e8e8")
    info_label.pack(fill=ts.X, padx=5, pady=5)

    map_widget = tkintermapview.TkinterMapView(right_frame, width=400, height=400, corner_radius=0)
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    map_widget.pack(fill=ts.BOTH, expand=True)

    # Default to HKMU Ho Man Tin Campuses, adjust zoom
    o_lat = c.get_campus("MC").lat + c.get_campus("IOH").lat + c.get_campus("JCC").lat + c.get_campus("HMT_PLAZA").lat
    o_lon = c.get_campus("MC").lon + c.get_campus("IOH").lon + c.get_campus("JCC").lon + c.get_campus("HMT_PLAZA").lon
    map_widget.set_position(o_lat / 4, o_lon / 4)
    map_widget.set_zoom(17)
    
    # Reload Map Function
    def reload_map():
        selected_indices = listbox.curselection()
        if selected_indices and selected_indices[0] < len(displayed_restaurants):
            # A restaurant is currently selected, center map on it instead of resetting everything
            r = displayed_restaurants[selected_indices[0]]
            map_widget.delete_all_marker()
            map_widget.set_position(r.lat, r.lon)
            map_widget.set_zoom(17)
            map_widget.set_marker(r.lat, r.lon, text=r.name)
        else:
            # No restaurant selected, do a full map reset to default coordinates
            map_widget.delete_all_marker()
            o_lat = c.get_campus("MC").lat + c.get_campus("IOH").lat + c.get_campus("JCC").lat + c.get_campus("HMT_PLAZA").lat
            o_lon = c.get_campus("MC").lon + c.get_campus("IOH").lon + c.get_campus("JCC").lon + c.get_campus("HMT_PLAZA").lon
            map_widget.set_position(o_lat / 4, o_lon / 4)
            map_widget.set_zoom(17)

    # Create Reload Button and place it hovering on the top right
    reload_btn = ts.Button(map_widget, text="↻ Reload Map", command=reload_map, bg="white", activebackground="#f0f0f0", relief=ts.RAISED, bd=1)
    reload_btn.place(relx=1.0, anchor=ts.NE, x=-10, y=10)

    displayed_restaurants = []

    # Define the search function
    def perform_search():
        listbox.delete(0, ts.END)
        displayed_restaurants.clear()
        
        query = search_var.get().lower()
        results_found = False
        
        for r in repo.get_all_restaurants():
            match = query in r.name.lower() or query in r.cuisines.lower()
            if query == "" or match:
                listbox.insert(ts.END, f"{r.name} - {r.cuisines} (rating {r.rating})")
                displayed_restaurants.append(r)
                results_found = True
                
        if not results_found:
            listbox.insert(ts.END, "No matching restaurants found for your query.")

    def on_restaurant_select(event):
        # Find which item is clicked
        selected_indices = listbox.curselection()
        if not selected_indices:
            return
            
        index = selected_indices[0]
        # Make sure don't crash if they click the "No matching..." text
        if index < len(displayed_restaurants):
            r = displayed_restaurants[index]
            lat = r.lat
            lon = r.lon
            # Place map marker
            map_widget.delete_all_marker()
            map_widget.set_position(lat, lon)
            map_widget.set_zoom(17)
            map_widget.set_marker(lat, lon, text=r.name)

            # Update info card
            details_text = (
                f"Name: {r.name}\n"
                f"Address/Location: {r.location}\n"
                f"Cuisine: {r.cuisines}\n"
                f"Dietary Tags: {r.dietary_tags}\n"
                f"Price Level: {int(r.price_level) * '$'+ (3 - int(r.price_level)) * ' ·'} | Rating: {int(r.rating) * '★ ' + (5 - int(r.rating)) * '☆ '}\n"
                f"Opening Hours: {w.textformat(r.weekly_hours)}\n"
            )
            info_var.set(details_text)

    listbox.bind("<<ListboxSelect>>", on_restaurant_select)


    def block_event(event):
        return "break"
    
    listbox.bind("<Up>", block_event)
    listbox.bind("<Down>", block_event)

    ts.Button(search_frame, text="Search", command=perform_search, bg="#4CAF50", fg="white").pack(side=ts.LEFT)
    # Populate the list initially
    perform_search()