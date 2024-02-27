from datetime import datetime


class Habit:
    def __init__(self, habit_name, habit_date, periodicity, task_specification,
                 current_streak, longest_streak, broken_streak, completed_date=None,
                 not_completed_date=None, last_update=None):
        """
        Creates a Habit object with the respective data.
        :param habit_name: name of the habit
        :param habit_date: the day when the habit was created
        :param periodicity: daily, weekly, or monthly
        :param task_specification: a short description of the habit
        :param current_streak: number of periods a habit has been done in a row
        :param longest_streak: the biggest number of periods a habit had been done in a row for the entire time
        :param broken_streak: number of periods a habit has NOT been done in a row
        :param completed_date: the date when the habit was last checked off
        :param not_completed_date: the date when the habit was last NOT completed
        :param last_update: the date when the habit was last checked off
        """
        self.habit_name = habit_name
        self.habit_date = habit_date
        self.periodicity = periodicity
        self.task_specification = task_specification
        self.current_streak = current_streak
        self.longest_streak = longest_streak
        self.broken_streak = broken_streak
        self.completed_date = completed_date if completed_date is not None else []
        self.not_completed_date = not_completed_date if not_completed_date is not None else []
        self.last_update = last_update

    def habit_completion_check(self):
        """
        Checks if the task has already been completed before the user can check it off.
        """
        today = datetime.now().date()

        if self.last_update is None:
            return False

        if self.periodicity == 'daily':
            if self.last_update == today:
                return True
            else:
                return False

        elif self.periodicity == 'weekly':
            if self.last_update is (today - self.last_update).days < 7:
                return True
            else:
                return False

        elif self.periodicity == 'monthly':
            if self.last_update is today.month == self.last_update.month:
                return True
            else:
                return False

    def check_habit_off(self):
        """
        Checks the chosen habit off for current time period, updates the longest streak, current
        streak and broken streak depending on task completion. If the habit has already been completed, the method
        prints it out to a user.
        """
        today = datetime.now().date()

        import database
        database.update_habits()

        if self.habit_completion_check():
            print(f"You have already completed {self.habit_name} for this time period.")
            return

        if self.periodicity == 'daily':
            self.last_update = today
            if self.last_update == today:
                self.current_streak += 1
                self.broken_streak = 0
                self.completed_date = today.strftime("%d.%m.%Y")
                print('Now you have completed this habit!')
            else:
                self.broken_streak += 1
                self.current_streak = 0

        elif self.periodicity == "weekly":
            if self.last_update is None or (today - self.last_update).days >= 7:
                self.last_update = today
                if self.last_update == today:
                    self.current_streak += 1
                    self.broken_streak = 0
                    self.completed_date = today.strftime("%d.%m.%Y")
                    print('Now you have completed this habit!')
                else:
                    self.broken_streak += 1
                    self.current_streak = 0
                    self.not_completed_date = today.strftime("%d.%m.%Y")

        elif self.periodicity == 'monthly':
            if self.last_update is None or today.month != self.last_update.month:
                self.last_update = today
                if self.last_update == today:
                    self.current_streak += 1
                    self.broken_streak = 0
                    self.completed_date = today.strftime("%d.%m.%Y")
                    print('Now you have completed this habit!')
                else:
                    self.broken_streak += 1
                    self.current_streak = 0
                    self.not_completed_date = today.strftime("%d.%m.%Y")

        self.longest_streak = max(self.current_streak, self.longest_streak)
        self.last_update = self.last_update.strftime("%d.%m.%Y")

        database.check_habit_off(self.current_streak, self.longest_streak, self.broken_streak,
                                 self.completed_date, self.not_completed_date, self.last_update,
                                 self.habit_name)
