import tkinter as tk
from tkinter import ttk
from datetime import datetime
from croniter import croniter
import time
import os
from tkinter import simpledialog


end_date = None

def schedule_capture(hourly_input, minute_input):
    global end_date
    # get the current date and timeµ
    if end_date is None:
        print("end date is none")
    else:
        #scedule the capture
        print("end date is not none")
        print("end date: ", end_date)
        print("hourly_input: ", hourly_input)
        print("minute_input: ", minute_input)

        # get the current date and time
        now = datetime.now()
        print("now: ", now)


        # get the end date and time
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        print("end_date: ", end_date)

        # get the hour and minute
        hour = int(hourly_input.get())
        minute = int(minute_input.get())

        # create a cron string
        cron_string = str(minute) + " " + str(hour) + " * * *"

        # create a cron iterator
        cron = croniter(cron_string, now)

        # close ths window
        


    

    print ("hourly_input: ", hourly_input , minute_input, end_date)


def get_end_date(result_label):
    global end_date
    end_date = simpledialog.askstring("Input", "Enter end date (YYYY-MM-DD):")
    print("end_date: ", end_date)
    result_label.config(text=end_date)


def schedule_window():
    global end_date

    new_window = tk.Toplevel()
    new_window.title("Scheduling")

    # give the windoz a size 
    new_window.geometry("400x200")

    button_frame = tk.Frame(new_window)
    button_frame.grid(row=0, column=0, columnspan=2, sticky="ew")


    result_label = tk.Label(button_frame, text="Select a end date")
    result_label.grid(row=1, column=0, padx=2, pady=2)

    select_end_date = ttk.Button(button_frame, text="Select end date", command= lambda: get_end_date(result_label))
    select_end_date.grid(row=1, column=1, padx=2, pady=2)

    # create a label for the hourly input
    hourly_label = tk.Label(button_frame, text="Enter a hourly interval")
    hourly_label.grid(row=2, column=0, padx=2, pady=2)

    # input field for hous
    hourly_input = tk.Entry(button_frame)
    hourly_input.grid(row=2, column=1, padx=2, pady=2)

    minute_label = tk.Label(button_frame, text="Enter a minute interval")
    minute_label.grid(row=3, column=0, padx=2, pady=2)
    
    # input field for minute
    minute_input = tk.Entry(button_frame)
    minute_input.grid(row=3, column=1, padx=2, pady=2)
    
    # create a button to schedule the capture
    schedule_button = ttk.Button(button_frame, text="Schedule", command=lambda: schedule_capture(hourly_input, minute_input))
    schedule_button.grid(row=4, column=0, padx=2, pady=2)

    
    # Start the Tkinter event loop
    new_window.mainloop()

    return "this is a test"