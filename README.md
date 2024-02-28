# Habit Tracker

This **Habit Tracker** project is designed to make tracking habits easier, allowing you to monitor your progress over time and providing a convenient way to stay organized and motivated. You can find information on how to install and use it below.

## Features

- **Creating Habits**: Users can add new habits, specifying their name, frequency (daily, weekly, monthly), and description.
- **Completing Habits**: Habits are updated automatically and can be checked off by the user.
- **Viewing Data**: Users can view information over their habits, including longest streaks, completed and not completed streaks.
- **Building Graphs**: The generated graphs allow users to see how their habit completion rate changed over time.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/pp0lina/habitTracker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd habitTracker
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python main.py
   ```

## Usage

1. Once the application is run, the app greets a user and shows a list of commands with their respective numbers.
2. This list includes creating a habit, checking a habit off, adding/deleting a tasks, viewing habit statistics etc. To execute a command, enter its number into the CLI.
3. To create a new habit, type 2 into the CLI. Then type the name of your new habit, choose periodicity (1 - daily, 2 - weekly, or 3 - monthly) and add a little description.
4. After this, your new habit is created, so you can check the list of all your current habits (type 4), check your new habit off (type 1), or use other functionality.
5. If you want to view the list of possible commands again, type /help.

## Test data

The required database is initialised automatically once the application is run. However, this database also includes 5 pre-defined habits and test data for 4 weeks which can affect your program usage. 
The test data can be checked in the test.py file. Bear in mind that the data there is not updated while the project is not used, so and it can influence the tests.

## Contributing

This project was built for educational purposes, so feel free to contribute to it!
