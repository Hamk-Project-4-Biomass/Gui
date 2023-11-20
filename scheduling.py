import tkinter as tk
from tkinter import ttk
from datetime import datetime
from croniter import croniter
import time
import os
from tkinter import simpledialog


end_date = None

def schedule_capture(hourly_input, minute_input, end_date):
    # get the current date and time
    # if the user has selected hourly
    print ("hourly_input: ", hourly_input , minute_input, end_date)


def get_end_date():
    global end_date
    end_date = simpledialog.askstring("Input", "Enter end date (YYYY-MM-DD):")

def schedule_window():
    global end_date

    new_window = tk.Toplevel()
    new_window.title("Scheduling")

    button_frame = tk.Frame(new_window)
    button_frame.grid(row=0, column=0, columnspan=2, sticky="ew")


    result_label = tk.Label(new_window, text="scedule")
    result_label.grid(row=1, column=0, padx=2, pady=2)

    select_end_date = ttk.Button(button_frame, text="Select end date", command=get_end_date)
    select_end_date.grid(row=0, column=0, padx=2, pady=2)

    # input field for hous
    hourly_input = tk.Entry(button_frame)
    hourly_input.grid(row=1, column=0, padx=2, pady=2)

    # input field for minute
    minute_input = tk.Entry(button_frame)
    minute_input.grid(row=2, column=0, padx=2, pady=2)
    
    # create a button to schedule the capture
    schedule_button = ttk.Button(button_frame, text="Schedule", command=schedule_capture(hourly_input, minute_input, end_date))
    schedule_button.grid(row=3, column=0, padx=2, pady=2)

    
    # Start the Tkinter event loop
    new_window.mainloop()