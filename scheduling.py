import tkinter as tk
from tkinter import ttk
from datetime import datetime
from croniter import croniter
import time
import os
from tkinter import simpledialog


end_date = None
result_cron_var = None

class ScheduleWindow(tk.Toplevel):

    def __init__(self,parent,callback):
        super().__init__(parent)


        # new_window = tk.Toplevel()
        self.title("Scheduling")

        # give the windoz a size 
        self.geometry("400x200")

        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=0, columnspan=2, sticky="ew")


        result_label = tk.Label(button_frame, text="Select a end date")
        result_label.grid(row=1, column=0, padx=2, pady=2)

        select_end_date = ttk.Button(button_frame, text="Select end date", command= lambda: self.get_end_date(result_label))
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
        schedule_button = ttk.Button(button_frame, text="Schedule", command=lambda: self.schedule_capture(hourly_input, minute_input))
        schedule_button.grid(row=4, column=0, padx=2, pady=2)

        ok_button = tk.Button(button_frame, text="OK", command=self.on_ok_button_click)
        ok_button.grid(row=5, column=0, padx=2, pady=2)

        # Store the callback function
        self.callback = callback

    def on_ok_button_click(self):
        global result_cron_var
        global end_date
        # Perform any necessary processing before destroying the window
        result_value = result_cron_var

        # Call the callback function in the parent window with the result
        self.callback(result_value, end_date)

        # Destroy the child window
        self.destroy()

    def schedule_capture(self,hourly_input, minute_input):
        global end_date
        global result_cron_var 
        result_cron_var = tk.StringVar()
        # get the current date and timeµ
       
        # get the hour and minute
        hour = int(hourly_input.get())
        minute = int(minute_input.get())

        #scedule the capture
        print("end date is not none")
        print("end date: ", end_date)
        print("hourly_input: ", hour)
        print("minute_input: ", minute)

        # get the current date and time
        now = datetime.now()
        print("now: ", now)


        # get the end date and time
        if end_date is not None:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        print("end_date: ", end_date)

        # create a cron string
        result_cron_var = str(minute) + " " + str(hour) + " * * *"

        print ("complete end time: ", end_date," capture every: ",hour ,":", minute, " cron string: ", result_cron_var)


    def get_end_date(self,result_label):
        global end_date
        end_date = simpledialog.askstring("Input", "Enter end date (YYYY-MM-DD):")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        print("end_date: ", end_date)
        result_label.config(text=end_date)
