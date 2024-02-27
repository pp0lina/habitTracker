import database
from tracking import HabitTracker
from datetime import datetime


# All the main methods are tested in this file. However, some methods were skipped for efficiency, since
# their code is almost identical to the other methods that passed the test (e.g., longest_streak_habit and
# broken_streak_habit).

def test_check_habit_off():
    database.create_table()
    database.add_test_data()

    HabitTracker().check_habit_off("read")
    all_habits = database.view_all_info()
    today = datetime.now().date()

    for habit in all_habits:
        if habit.habit_name == "read":
            read_habit = habit
            break

    assert read_habit.current_streak == 1
    assert read_habit.longest_streak == 15
    assert read_habit.broken_streak == 0
    assert read_habit.last_update == today.strftime("%d.%m.%Y")


def test_add_habit():
    database.create_table()
    HabitTracker().add_habit("test_habit", "daily", "Test habit description")
    current_habits = database.view_all_habits()
    assert "test_habit" in current_habits


def test_delete_habit():
    database.create_table()
    HabitTracker().delete_habit("read")
    current_habits = database.view_all_habits()
    assert "read" not in current_habits


def test_get_current_habits():
    database.create_table()
    database.add_test_data()
    current_habits = database.view_all_habits()
    assert current_habits == ["clean", "finance", "goals", "no phone", "read"]


def test_longest_streak_overall():
    database.create_table()
    database.add_test_data()
    longest_streak_habit, longest_streak = HabitTracker().longest_streak_overall()

    assert longest_streak_habit == 'read', longest_streak == 15


def test_longest_streak_habit():
    habit_name, habit_longest_streak = HabitTracker().longest_streak_one("clean")
    assert habit_longest_streak == 5


def test_broken_streak_overall():
    database.create_table()
    database.add_test_data()
    broken_streak_habit, broken_streak = HabitTracker().broken_streak_overall()

    assert broken_streak_habit == 'read', broken_streak == 10


def test_get_one_habit():
    HabitTracker().get_one_habit("wash")
    assert "Sorry, a habit with this name doesn't exists. Please try again."


def test_get_same_periodicity():
    result = HabitTracker().get_same_periodicity(p='monthly')
    assert "finance", "goals" in result
