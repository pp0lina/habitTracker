from collections import defaultdict
from datetime import datetime

import database
from tracking import HabitTracker
from statistics import Statistics

# the sqlite3 database is launched, the test data is added, all data is updated when the program starts
database.create_table()
database.add_test_data()
database.update_habits()

# get time from the user to greet the user based on their time in UTC
current_time = datetime.now().hour

if 5 <= current_time < 12:
    print('\nGood morning!')
elif 12 <= current_time < 18:
    print('\nGood afternoon!')
elif 18 <= current_time < 22:
    print('\nGood evening!')
else:
    print('\nGood night!')

print("\nDon't wait for opportunity, create it. Let's start.")

# makes the list of possible commands visible to the user
print("\nHere's a list of things you can do. Just type in the command number.")
print('1 - Check off a task.')
print('2 - Create a new task.')
print('3 - Delete a task.')
print('4 - Get a list of all current habits.')
print('5 - Get the longest habit streak out of all the existing habits.')
print('6 - Get the longest habit streak of one chosen habit.')
print('7 - Get the most difficult habit to complete overall.')
print('8 - Get the most skipped days of a chosen habit.')
print('9 - Get all completion habits info.')
print('10 - Get all broken habits info.')
print('11 - Get data from a specific habit.')
print('12 - Get all habits of a specific periodicity.')
print('13 - Get certain habit statistics.')
print('14 - Get overall habit statistics.')
print('15 - Get all habits info of the entire period of using the program.')
print('16 - Exit the program.')
print("\nType /help if you want to see this list again.")

# get the command number from the user and execute it
while True:
    choice = input()

    match choice:

        case '1':
            # Marks the task as completed in the habit tracker
            habit_name = input('Write the name of the habit you have completed: ')
            HabitTracker().check_habit_off(habit_name)
            print('\nWell done. You have completed this habit.')

        case '2':
            # Creates a new task in the habit tracker and database, asks a user for habit name, periodicity,
            # and habit specification
            habit_name = input("Please type the name of your new habit: ")
            while True:
                p = input("What is this habit's periodicity? "
                          "Type 1 for daily, 2 for weekly, or 3 for monthly.\n")
                if p == '1':
                    periodicity = 'daily'
                    break
                elif p == '2':
                    periodicity = 'weekly'
                    break
                elif p == '3':
                    periodicity = 'monthly'
                    break
                else:
                    print("You can only type 1, 2, or 3. Please try again.")
            task_specification = input('Please enter a task description: ')

            HabitTracker().add_habit(habit_name, periodicity, task_specification)
            print('Task added successfully!')

        case '3':
            # deletes a habit from the database based on the habit name input
            habit_name = input('Which habit would you like to delete?\n')
            HabitTracker().delete_habit(habit_name)

        case '4':
            # returns the names of all habits that a user has in the database
            print('Your current habits are:')
            for habit in database.view_all_habits():
                print(habit.__str__())

        case '5':
            # gets the longest habit completion streak among all habits
            longest_streak_habit, longest_streak = HabitTracker().longest_streak_overall()
            print(f'Your longest streak overall is {longest_streak_habit} with {longest_streak} completed periods.')

        case '6':
            # gets the longest habit completion streak for one specified habit
            habit_name = input('For which habit would you like to show the longest streak?\n')
            habit_name, habit_longest_streak = HabitTracker().longest_streak_one(habit_name)
            print(f"The habit '{habit_name}' has the longest streak of {habit_longest_streak} periods.")

        case '7':
            # gets the habit that has not been done for the longest period among all habits
            broken_streak_habit, broken_streak = HabitTracker().broken_streak_overall()
            print(f'Your most difficult habit to complete overall is {broken_streak_habit} with {broken_streak} '
                  f'skipped periods.')

        case '8':
            # gets the number of periods a certain habit has been skipped for
            habit_name = input('For which habit would you like to show the skipped periods?\n')
            habit_name, habit_broken_streak = HabitTracker().broken_streak_one(habit_name)
            print(f"The habit '{habit_name}' has been skipped for {habit_broken_streak} periods.")

        case '9':
            # gets the longest habit completion streak for each habit
            print("Here's some information over your longest streaks for each habit:")
            streaks_dict = HabitTracker().longest_streak_all()
            for habit_name, longest_streak in streaks_dict.items():
                print(f"{habit_name}: {longest_streak}")

        case '10':
            # gets the number of periods that each habit has been skipped for
            print("Here's some information over your non-completed streaks for each habit:")
            streaks_dict = HabitTracker().broken_streak_all()
            for habit_name, broken_streak in streaks_dict.items():
                print(f"{habit_name}: {broken_streak}")

        case '11':
            # returns data from a certain habit specified by user
            habit_name = input("Please enter the name of the habit you would like to receive data from.\n")
            habit_info = HabitTracker().get_one_habit(habit_name)
            if habit_info:
                print("Here's the information for the habit:", habit_name)
                print("Habit Name:", habit_info.habit_name)
                print("Habit Date:", habit_info.habit_date)
                print("Periodicity:", habit_info.periodicity)
                print("Task Specification:", habit_info.task_specification)
                print("Current Streak:", habit_info.current_streak)
                print("Longest Streak:", habit_info.longest_streak)
                print("Broken Streak:", habit_info.broken_streak)
            else:
                print("Sorry, a habit with this name doesn't exist. Please try again.")

        case '12':
            # returns a list of habits with the same periodicity (daily, weekly, or monthly) based on user input
            p = input("What is the periodicity which habits you'd like to view?"
                      "\nType daily, weekly, or monthly: ").lower().strip()
            if HabitTracker().get_same_periodicity(p):
                print("Here are the habits with the specified periodicity:")
                for habit in HabitTracker().get_same_periodicity(p):
                    print(habit.habit_name)

        case '13':
            # returns a graph with habit completion rate over time for a certain habit specified by user
            habit_name = input("Please type in the habit name that you want to see statistics from: ")
            completed_dates = defaultdict(int)
            not_completed_dates = defaultdict(int)
            if Statistics().build_graph_one(habit_name, completed_dates, not_completed_dates):
                pass
            else:
                print("Sorry, the habit with this name does not exist.")

        case '14':
            # returns a graph with habit completion rate over time for all habits in the database
            Statistics.build_graph_all()

        case '15':
            # returns all habit data that a program has
            all_habits_data = HabitTracker().get_all_habits_data()
            if all_habits_data:
                print("Here's the information for all habits:")
                for habit_data in all_habits_data:
                    print("Habit Name:", habit_data["Habit Name"])
                    print("Habit Date:", habit_data["Habit Date"])
                    print("Periodicity:", habit_data["Periodicity"])
                    print("Task Specification:", habit_data["Task Specification"])
                    print("Current Streak:", habit_data["Current Streak"])
                    print("Longest Streak:", habit_data["Longest Streak"])
                    print("Broken Streak:", habit_data["Broken Streak"])
                    print()  # Add a new line between habits
            else:
                print("No habit data available.")

        case '16':
            # terminates the program execution
            print('Exiting the program...')
            exit()

        case '/help':
            # makes the list of commands visible to the user
            print("Here's a list of things you can do:")
            print('1 - Check off a task.')
            print('2 - Create a new task.')
            print('3 - Delete a task.')
            print('4 - Get a list of all current habits.')
            print('5 - Get the longest habit streak out of all the existing habits.')
            print('6 - Get the longest habit streak of one chosen habit.')
            print('7 - Get the most difficult habit to complete overall.')
            print('8 - Get the most skipped days of a chosen habit.')
            print('9 - Get all completion habits info.')
            print('10 - Get all broken habits info.')
            print('11 - Get data from a specific habit.')
            print('12 - Get all habits of a specific periodicity.')
            print('13 - Get certain habit statistics.')
            print('14 - Get overall habit statistics.')
            print('15 - Get all habits info of the entire period of using the program.')
            print('16 - Exit the program.')
            print("\nType /help if you want to see this list again.")

        case _:
            # makes the list of commands visible to the user if the input value does not match any of the previous cases
            print("This command is not on the list! Here's what you can do:")
            print('1 - Check off a task.')
            print('2 - Create a new task.')
            print('3 - Delete a task.')
            print('4 - Get a list of all current habits.')
            print('5 - Get the longest habit streak out of all the existing habits.')
            print('6 - Get the longest habit streak of one chosen habit.')
            print('7 - Get the most difficult habit to complete overall.')
            print('8 - Get the most skipped days of a chosen habit.')
            print('9 - Get all completion habits info.')
            print('10 - Get all broken habits info.')
            print('11 - Get data from a specific habit.')
            print('12 - Get all habits of a specific periodicity.')
            print('13 - Get certain habit statistics.')
            print('14 - Get overall habit statistics.')
            print('15 - Get all habits info of the entire period of using the program.')
            print('16 - Exit the program.')
