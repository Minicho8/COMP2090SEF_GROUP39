
import tkinter as tk
import viewBuilder as vb
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
    
    # Build GUI using viewBuilder
    vb.build_main_view(root, repo)

    # start the tkinter screen loop
    root.mainloop()

# start the system
if __name__ == "__main__":
    main()

