import calendar
from datetime import datetime, timedelta
from collections import defaultdict


def get_birthdays_per_week(users, run_weekends=False):
    '''Prints day of the week and name of the person who has a birthday that day for the next week, doesn't work on weekends.
        Parameters:
        - users (list of user dicts) - [{"name": "Bill Gates", "birthday": datetime(1955, 10, 28)},...]
        - run_weekends (bool) - default = False, if set to True, function will run on weekends
        Output:
        - doesn't retutrn anything
        - prints weekday: username for every user who has birhday next week sorted Mo -> Fr, Sa & Su are moved to the next Mo
    '''
    users_by_weekday = defaultdict(list)
    today = datetime.now().date()
    curr_weekday = today.weekday()

    def is_monday(day_number: int):
        return day_number == 0

    def is_weekend(day_number: int):
        return day_number == 5 or day_number == 6

    if is_weekend(curr_weekday) and not run_weekends:
        print((f"Today is {calendar.day_name[curr_weekday]} and we don't do evaluations"
              "on weekends. Enjoy your free time!"))
        return

    weekend = timedelta(days=2 if is_monday(curr_weekday) else 0)
    week = timedelta(days=7)
    for user in users:
        birthday_this_year = user["birthday"].replace(year=today.year).date()
        # including past weekend and exluding next weekend if day is Monday
        if (birthday_this_year >= today - weekend and
                birthday_this_year < today + week - weekend):
            users_by_weekday[birthday_this_year.weekday()].append(user["name"])

    # move the weekend birthdays to Monday
    for weekday in sorted(users_by_weekday.keys()):
        if is_weekend(weekday):
            users_by_weekday[0].extend(users_by_weekday.pop(weekday))

    # sorting the result by the day of the week => Mo will always come first
    for d, n in sorted(users_by_weekday.items()):
        print(f"{calendar.day_name[d] + ':':<10} {', '.join(n)}")


if __name__ == "__main__":
    # Get the current date
    current_date = datetime.now()

    # Calculate birthdays for the users
    users = [
        {"name": "John Doe", "birthday": current_date +
            timedelta(days=3)},  # Birthday 3 days from today
        {"name": "Alice Smith", "birthday": current_date + \
            timedelta(days=5)},  # Birthday 5 days from today
        {"name": "Bob Johnson", "birthday": current_date + \
            timedelta(days=7)},  # Birthday 7 days from today
        {"name": "Emma Williams", "birthday": current_date + \
            timedelta(days=15)},  # Birthday 15 days from today
        {"name": "Sarah Brown", "birthday": current_date + \
            timedelta(days=20)},  # Birthday 20 days from today
    ]

    get_birthdays_per_week(users, run_weekends=True)
