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

    valid_date = False
    default_date = True

    def is_valid_cron(self, croniter_string):
        try:
            croniter(croniter_string)
            return True
        except ValueError:
            return False

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

        # create a label for thecron input
        cron_label = tk.Label(button_frame, text="Enter a cron expression interval")
        cron_label.grid(row=2, column=0, padx=2, pady=2)

        # create a label for the cron result
        self.cron_result_label = tk.Label(button_frame, text=f"Cron validation result: None")
        self.cron_result_label.grid(row=3, column=0, padx=2, pady=2)

        # input field for cron
        cron_input = tk.Entry(button_frame)
        cron_input.grid(row=2, column=1, padx=2, pady=2)
        
        # create a button to schedule the capture
        schedule_button = ttk.Button(button_frame, text="Validate", command=lambda: self.schedule_capture(cron_input))
        schedule_button.grid(row=4, column=0, padx=2, pady=2)

        self.ok_button = tk.Button(button_frame, text="OK", state=tk.DISABLED ,command=self.on_ok_button_click)
        self.ok_button.grid(row=5, column=0, padx=2, pady=2)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.grid(row=6, column=0, padx=2, pady=2)

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

    def schedule_capture(self,cron_input):
        global end_date
        global result_cron_var 
        result_cron_var = tk.StringVar()
        
        if self.is_valid_cron(cron_input.get()):
            result_cron_var = cron_input.get()
            self.cron_result_label.config(text=f"Cron and date validation result: Valid")
            if self.valid_date or self.default_date:
                self.ok_button.config(state=tk.NORMAL)
            else: 
                self.ok_button.config(state=tk.DISABLED)
        else:
            self.cron_result_label.config(text=f"Cron and date validation result: Invalid")
            self.ok_button.config(state=tk.DISABLED)
            return None
        # get the current date and timeµ

        #scedule the capture
        if end_date is not None:
            print("end date is not none")
        print("end date: ", end_date)
    

        # get the current date and time
        now = datetime.now()
        print("now: ", now)

        print("end_date: ", end_date)

        print ("complete end time: ", end_date, " cron string: ", result_cron_var)


    def get_end_date(self,result_label):
        global end_date
        end_date_dt = None
        self.ok_button.config(state=tk.DISABLED)
        end_date_str = simpledialog.askstring("Input", "Enter end date (YYYY-MM-DD):")

        if end_date_str != '' and end_date_str is not None:
            try:
                # Try to parse the date string
                end_date_dt = datetime.strptime(end_date_str, "%Y-%m-%d")
                print("end_date is in the correct format")
                result_label.config(text=end_date_str)
                end_date = end_date_dt
                self.valid_date = True
                self.default_date = False
                result_label.config(text=end_date)
            except ValueError:
                result_label.config(text="Invalid date format")
                self.valid_date = False
                self.default_date = False
        else: 
            result_label.config(text="Date set to None")
            self.valid_date = True
            self.default_date = False
            end_date = None 
