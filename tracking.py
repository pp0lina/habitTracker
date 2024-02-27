import json

import database
from datetime import datetime

from habits import Habit


class HabitTracker:

    def __init__(self):
        # Imports the database and initializes the needed functionality.
        self.database = database.view_all_info()

    def check_habit_off(self, habit_name):
        """
        Checks the chosen task off for current time period, updates the longest streak, current
        streak and broken streak depending on task completion.
        """
        for habit in self.database:
            if habit_name == habit.habit_name:
                habit.check_habit_off()
                return
        print("Habit not found.")

    def add_habit(self, habit_name, periodicity, task_specification):
        """
        This method adds a habit to the database if no habit with such name exists yet. If it does,
        the user will see this information via the print command.
        """
        existing_habits = self.get_all_habits_data()
        if habit_name in existing_habits:
            print("Sorry, a habit with this name already exists. Please try again.")
            return
        new_habit = Habit(habit_name, datetime.now().date(), periodicity, task_specification,
                          0, 0, 0, json.dumps([]),
                          json.dumps([]), None)
        database.add_habit(new_habit)
        self.__init__()

    def delete_habit(self, habit_name):
        # This method deletes a habit from the database
        for habit in self.database:
            if habit.habit_name == habit_name:
                database.delete_habit(habit_name)
                print("Habit successfully deleted.")
                self.__init__()
                return
        print("Sorry, a habit with this name doesn't exists. Please try again.")

    def longest_streak_overall(self):
        # This method returns the longest streak among all the exiting habits
        longest_streak_habit = None
        longest_streak = 0

        for habit in self.database:
            if habit.longest_streak > longest_streak:
                longest_streak = habit.longest_streak
                longest_streak_habit = habit.habit_name

        return longest_streak_habit, longest_streak

    def longest_streak_one(self, habit_name):
        # This method returns the longest habit streak of one chosen habit
        found_habit = False
        for habit in self.database:
            if habit.habit_name == habit_name:
                habit_longest_streak = habit.longest_streak
                return habit_name, habit_longest_streak

        if not found_habit:
            print("Sorry, a habit with this name does not exist.")

    def broken_streak_overall(self):
        """
        This method returns the most days a habit was not completed in a row among all the
        exiting tasks. Therefore, this method gets the most difficult habit to complete overall.
        """
        broken_streak_habit = None
        broken_streak = 0

        for habit in self.database:
            if habit.broken_streak > broken_streak:
                broken_streak = habit.broken_streak
                broken_streak_habit = habit.habit_name

        return broken_streak_habit, broken_streak

    def broken_streak_one(self, habit_name):
        # This method returns the biggest number of days that a chosen habit has not been done for.
        found_habit = False
        for habit in self.database:
            if habit.habit_name == habit_name:
                habit_broken_streak = habit.broken_streak
                return habit_name, habit_broken_streak

        if not found_habit:
            print("Sorry, a habit with this name does not exist.")

    def longest_streak_all(self):
        # This method returns a dictionary of habits with their longest completed streaks.
        return {habit.habit_name: habit.longest_streak for habit in self.database}

    def broken_streak_all(self):
        # This method returns a dictionary of habits with their broken (missed) streaks.
        return {habit.habit_name: habit.broken_streak for habit in self.database}

    def get_one_habit(self, habit_name):
        """
        This method gets full information from the one habit that was chosen by the user.
        """
        found_habit = False
        for habit in self.database:
            if habit.habit_name == habit_name:
                return habit
            found_habit = True
        if not found_habit:
            print("Sorry, a habit with this name doesn't exists. Please try again.")

    def get_same_periodicity(self, p):
        """
        This method filters the habit list based on the specified periodicity input by the user and returns
        the required data.
        """
        periodicity_filters = {
            'daily': lambda habit: [habit for habit in habit if habit.periodicity == 'daily'],
            'weekly': lambda habit: [habit for habit in habit if habit.periodicity == 'weekly'],
            'monthly': lambda habit: [habit for habit in habit if habit.periodicity == 'monthly']
        }

        if p in periodicity_filters:
            filtered_tasks = periodicity_filters[p](self.database)
            return filtered_tasks
        else:
            print("There is no such periodicity. Please try again.")
            return []

    def get_all_habits_data(self):
        """
        This method returns all habit information from the database.
        """
        all_habits_data = []
        for habit in self.database:
            habit_data = {
                "Habit Name": habit.habit_name,
                "Habit Date": habit.habit_date,
                "Periodicity": habit.periodicity,
                "Task Specification": habit.task_specification,
                "Current Streak": habit.current_streak,
                "Longest Streak": habit.longest_streak,
                "Broken Streak": habit.broken_streak
            }
            all_habits_data.append(habit_data)
        return all_habits_data
