# croniter_subprocess.py
from datetime import datetime, timedelta
from croniter import croniter
import time
import multiprocessing
import sys

class cron_job():

    def __init__(self, cron_string, end_date, callback, stop_event):
        self.cron_string = cron_string
        self.end_date = end_date
        self.callback = callback
        self.stop_event = stop_event
        self.time_until_next_execution = None

        process = multiprocessing.Process(target=self.launch_subprocess, args=( self.time_until_next_execution, ))
        process.start()

    def launch_subprocess(self):
        cron = croniter(self.cron_expression)

        while not self.stop_event.is_set() and (self.end_date is None or datetime.now() < self.end_date):

            next_execution = cron.get_next(datetime)
            current_time = datetime.now()

            if next_execution > current_time:
                self.time_until_next_execution = (next_execution - current_time).total_seconds()

                print(f"Waiting {self.time_until_next_execution} seconds until the next invocation")
                time.sleep(5)
            else:
                print(f"Invoking button at {current_time}")
                self.callback()
        else:
            print("Stopping the cron job")
            sys.exit(0)

    def set_stop_event(self):
        self.stop_event.set()
