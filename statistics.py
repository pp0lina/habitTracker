from collections import defaultdict
from datetime import datetime
import sqlite3

import database
import matplotlib.pyplot as plt
from matplotlib import style

style.use('dark_background')


class Statistics:
    """
    A class for generating habit tracker graphs from the data stored in databases.
    """

    def __init__(self):
        # Imports the database and initializes the needed functionality
        self.database = database.view_all_habits()

    def build_graph_one(self, habit_name, completed_dates, not_completed_dates):
        """
        This method build a graph for the specified habit and shows its completion rate over time. The x-axis represents
        dates, the y-axis represents habit completion rate (calculated as completed habit dates divided by all stored
        dates: both completed and not completed).
        """
        db = sqlite3.connect('HabitTracker.db')
        c = db.cursor()
        c.execute("SELECT completed_date, not_completed_date, habit_name FROM dates WHERE habit_name = ?",
                  (habit_name,))
        data = c.fetchall()

        if completed_dates is None:
            completed_dates = defaultdict(int)
        if not_completed_dates is None:
            not_completed_dates = defaultdict(int)

        for row in data:
            completed_date_str, not_completed_date_str = row[0], row[1]
            if completed_date_str:
                completed_date_str = completed_date_str.strip('"')
                completed_date = datetime.strptime(completed_date_str, "%d.%m.%Y")
                completed_dates[completed_date] += 1
            if not_completed_date_str:
                not_completed_date_str = not_completed_date_str.strip('"')
                not_completed_date = datetime.strptime(not_completed_date_str, "%d.%m.%Y")
                not_completed_dates[not_completed_date] += 1

        if not completed_dates and not not_completed_dates:
            print("Sorry, the habit with this name does not exist.")
            return False

        completion_rate = []
        total_habits = len(completed_dates) + len(not_completed_dates)
        if total_habits > 0:
            for date in sorted(set(completed_dates) | set(not_completed_dates)):
                completed_habits = completed_dates[date]
                completion_rate.append(completed_habits / total_habits)
        else:
            completion_rate = [0] * len(completed_dates)  # Avoid the zero division error

        dates = sorted(set(completed_dates) | set(not_completed_dates))
        plt.plot(dates, completion_rate, label=f'{habit_name} Completion Rate', color='red')
        plt.xlabel('Time')
        plt.ylabel('Completion Rate')
        plt.title(f'{habit_name} Completion Rate Over Time')
        plt.legend()
        plt.show()

        return True

    @staticmethod
    def build_graph_all():
        """
        This method build a graph from overall habit data and shows the completion rate over time. Again, the x-axis
        represents dates, while the y-axis represents habit completion rate (calculated as ALL completed habit dates
        divided by ALL stored dates: both completed and not completed).
        """
        db = sqlite3.connect('HabitTracker.db')
        c = db.cursor()
        c.execute("SELECT completed_date, not_completed_date FROM dates")
        data = c.fetchall()

        completed_dates = {}
        not_completed_dates = {}

        for row in data:
            completed_date_str, not_completed_date_str = row[0], row[1]
            if completed_date_str:
                completed_date_str = completed_date_str.strip('"')
                completed_date = datetime.strptime(completed_date_str, "%d.%m.%Y").date()
                completed_dates[completed_date] = completed_dates.get(completed_date, 0) + 1
            if not_completed_date_str:
                not_completed_date_str = not_completed_date_str.strip('"')
                not_completed_date = datetime.strptime(not_completed_date_str, "%d.%m.%Y").date()
                not_completed_dates[not_completed_date] = not_completed_dates.get(not_completed_date, 0) + 1

        completion_rate = []
        for date in sorted(set(completed_dates) | set(not_completed_dates)):
            completed_habits = completed_dates.get(date, 0)
            not_completed_habits = not_completed_dates.get(date, 0)
            completion_rate.append(completed_habits / (
                    completed_habits + not_completed_habits) if completed_habits + not_completed_habits > 0 else 0)

        dates = sorted(set(completed_dates) | set(not_completed_dates))
        plt.plot(dates, completion_rate, label=f'Average Completion Rate')
        plt.xlabel('Time')
        plt.ylabel('Completion Rate')
        plt.title(f'Average Completion Rate Over Time for All Habits')
        plt.legend()
        plt.show()
