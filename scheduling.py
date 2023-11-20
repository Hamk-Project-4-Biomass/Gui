import tkinter as tk
from tkinter import ttk

def perform_activity():
    return "This is an activity!"

def schedule_window():
    new_window = tk.Toplevel()
    new_window.title("Scheduling")

    # GUI elements for the new window
    label = tk.Label(new_window, text="Performing Activity:")
    label.pack()

    result_label = tk.Label(new_window, text=perform_activity())
    result_label.pack()

    # You can add more GUI elements here as needed
