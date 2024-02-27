import json
import sqlite3
from datetime import datetime, timedelta

from habits import Habit


def create_table():
    """
    Creates tables for habits and dates if they don't exist already. The data is stored in two separate tables for
    efficiency, given that one big table would have too many values and be complicated to manage because of dates.
    """
    db = sqlite3.connect('HabitTracker.db')
    c = db.cursor()
    c.execute("""DROP TABLE IF EXISTS habits""")
    c.execute("""DROP TABLE IF EXISTS dates""")
    c.execute("""CREATE TABLE IF NOT EXISTS habits (
            habit_name TEXT NOT NULL PRIMARY KEY,
            habit_date TEXT NOT NULL,
            periodicity TEXT,
            task_specification TEXT,
            current_streak INTEGER,
            longest_streak INTEGER,
            broken_streak INTEGER
            )""")
    c.execute("""CREATE TABLE IF NOT EXISTS dates (
                    habit_name TEXT NOT NULL,
                    completed_date text array TEXT,
                    not_completed_date text array TEXT,
                    last_update TEXT,
                    FOREIGN KEY (habit_name) REFERENCES habits(habit_name)
                    )""")
    db.commit()
    db.close()


def update_habits():
    """
    Updates habits. If the habit is not marked completed (checked off) in its respective period (day, week, or month),
    the habit streak is broken, current streak is set to 0 and the date is stored as the day when a habit was not done.
    """
    today = datetime.now()

    for habit in view_all_info():
        if habit.periodicity == 'daily':
            period = timedelta(days=1)
        elif habit.periodicity == 'weekly':
            period = timedelta(weeks=1)
        elif habit.periodicity == 'monthly':
            period = timedelta(days=30)

        # Check if last completed date is beyond the period
        if habit.last_update is not None:
            last_update = datetime.strptime(habit.last_update, "%d.%m.%Y")
            if today - last_update > period:
                habit.current_streak = 0
                habit.broken_streak += 1
                habit.not_completed_date = today.strftime("%d.%m.%Y")
        else:
            # if a habit is new, the last_update is set to None. In this case, not completed habit periods are counted
            # from the habit creation date.
            last_update = datetime.strptime(habit.habit_date, "%d.%m.%Y")
            if today - last_update > period:
                habit.current_streak = 0
                habit.broken_streak += 1
                habit.not_completed_date = today.strftime("%d.%m.%Y")

        db = sqlite3.connect('HabitTracker.db')
        c = db.cursor()

        c.execute("""UPDATE habits SET current_streak = ?, broken_streak = ? WHERE habit_name = ?""",
                  (habit.current_streak, habit.broken_streak, habit.habit_name))

        not_completed_date_str = json.dumps(habit.not_completed_date)

        c.execute("""UPDATE dates SET not_completed_date = ? WHERE habit_name = ?""",
                  (not_completed_date_str, habit.habit_name))

        db.commit()
        db.close()


def check_habit_off(current_streak, longest_streak, broken_streak, completed_date,
                    not_completed_date, last_update, habit_name):
    """
    This method checks off a habit and updates the databases.
    """
    db = sqlite3.connect('HabitTracker.db')
    c = db.cursor()
    c.execute("""UPDATE habits SET current_streak = ?, longest_streak = ?, broken_streak = ? 
                WHERE habit_name = ?""",
              (current_streak, longest_streak, broken_streak, habit_name))

    completed_date_str = json.dumps(completed_date)
    not_completed_date_str = json.dumps(not_completed_date)

    c.execute("""UPDATE dates SET completed_date = ?, not_completed_date = ?, last_update = ?
                WHERE habit_name = ?""", (completed_date_str, not_completed_date_str, last_update, habit_name))
    db.commit()
    db.close()


def add_habit(habit):
    """
    This method adds a habit with its respective values to the database.
    """
    db = sqlite3.connect('HabitTracker.db')
    c = db.cursor()
    c.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)""",
              (habit.habit_name, habit.habit_date, habit.periodicity,
               habit.task_specification, habit.current_streak, habit.longest_streak,
               habit.broken_streak))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              (habit.habit_name, habit.completed_date, habit.not_completed_date,
               habit.last_update))
    db.commit()
    db.close()


def delete_habit(habit_name):
    """
    Deletes a habit with its respective values from the database.
    """
    db = sqlite3.connect('HabitTracker.db')
    c = db.cursor()
    c.execute("""DELETE FROM habits WHERE habit_name = ?""", (habit_name,))
    c.execute("""DELETE FROM dates WHERE habit_name = ?""", (habit_name,))
    db.commit()
    db.close()


def view_all_habits():
    """
    Retrieves a list of all habit names.
    """
    db = sqlite3.connect('HabitTracker.db')
    c = db.cursor()
    c.execute("SELECT habit_name FROM habits")
    habits = c.fetchall()
    return [habit[0] for habit in habits]


def view_all_info():
    """
    Retrieves all habit information.
    """
    db = sqlite3.connect('HabitTracker.db')
    c = db.cursor()
    c.execute("SELECT * FROM habits")
    habits_data = c.fetchall()

    habits = []
    for habit_data in habits_data:
        habit = Habit(*habit_data)  # Create an instance of Habit class using tuple unpacking
        habit_name = habit_data[0]
        c.execute("SELECT completed_date, not_completed_date, last_update FROM dates WHERE habit_name = ?",
                  (habit_name,))
        dates = c.fetchone()
        if dates:
            completed_date = json.dumps(dates[0]) if dates[0] else "[]"
            not_completed_date = json.dumps(dates[1]) if dates[1] else "[]"
            last_update = (dates[2]) if dates[2] else None
            habit.completed_date = completed_date
            habit.not_completed_date = not_completed_date
            habit.last_update = last_update
        habits.append(habit)

    db.close()
    return habits


def add_test_data():
    """
    Adds test data for a period of 4 weeks to the database.
    """
    db = sqlite3.connect('HabitTracker.db')
    c = db.cursor()

    c.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)""",
              ("clean", "24.01.2024", "weekly", "Clean the apartment",
               5, 5, 0))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("clean", "24.01.2024", None, "24.01.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("clean", "31.01.2024", None, "31.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("clean", "07.02.2024", None, "07.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("clean", "14.02.2024", None, "14.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("clean", "21.02.2024", None, "21.02.2024"))

    c.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)""",
              ("finance", "21.01.2024", "monthly", "Review and plan your expenses",
               2, 2, 0))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("finance", "21.01.2024", None, "21.01.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("finance", "22.02.2024", None, "22.02.2024"))

    c.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)""",
              ("goals", "26.01.2024", "monthly", "Write down your current goals",
               1, 1, 0))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("goals", "26.01.2024", None, "26.01.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("goals", "26.02.2024", None, "26.02.2024"))

    c.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)""",
              ("no phone", "24.01.2024", "weekly", "Do not use the phone for the entire day",
               0, 1, 4))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("no phone", "25.01.2024", None, "25.01.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("no phone", None, "01.02.2024", "25.01.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("no phone", None, "08.02.2024", "25.01.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("no phone", None, "15.02.2024", "25.01.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("no phone", None, "22.02.2024", "25.01.2024"))

    c.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)""",
              ("read", "28.01.2024", "daily", "Read at least 30 minutes per day",
               0, 15, 9))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", None, "28.01.2024", "28.01.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", None, "29.01.2024", "28.01.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "30.01.2024", None, "30.01.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", None, "31.01.2024", "30.01.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "01.02.2024", None, "01.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "02.02.2024", None, "02.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "03.02.2024", None, "03.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "04.02.2024", None, "04.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "05.02.2024", None, "05.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "06.02.2024", None, "06.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "07.02.2024", None, "07.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "08.02.2024", None, "08.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "09.02.2024", None, "09.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "10.02.2024", None, "10.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "11.02.2024", None, "11.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "12.02.2024", None, "12.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "13.02.2024", None, "13.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "14.02.2024", None, "14.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", "15.02.2024", None, "15.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", None, "16.02.2024", "15.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", None, "18.02.2024", "15.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", None, "19.02.2024", "15.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", None, "20.02.2024", "15.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", None, "21.02.2024", "15.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", None, "22.02.2024", "15.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", None, "23.02.2024", "15.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", None, "24.02.2024", "15.02.2024"))
    c.execute("""INSERT INTO dates VALUES (?, ?, ?, ?)""",
              ("read", None, "25.02.2024", "15.02.2024"))

    db.commit()
    db.close()
