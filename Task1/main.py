
import tkinter as tk
import viewBuilder as build
import models as m
import dataService

def main():
    # Initialize the main tkinter window
    root = tk.Tk()
    root.title("Restaurant Search App")
    root.geometry("800x600")
    root.state("zoomed")
    

    # read the restaurant data from CSV file and build the linked list
    repo = dataService.CsvRestaurantRepository()
    repo.read_file()


    def show_home(criteria=None):
        for view in root.winfo_children():
            view.destroy()
        home_view = build.HomeView(root, repo, show_main, criteria)
        home_view.pack(fill=tk.BOTH, expand=True)
    
    def show_main(criteria):
        for view in root.winfo_children():
            view.destroy()
        main_view = build.MainView(root, repo, show_home, criteria)
        main_view.pack(fill=tk.BOTH, expand=True)
    
    show_home()
    # start the tkinter screen loop
    root.mainloop()

# start the system
if __name__ == "__main__":
    main()