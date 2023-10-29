# goitneo-python-hw-3-MCS3
Created for submission of the 3rd homwork assignment in the Tier 1 Python course
# Functionality of the CLI
The command should start with the listed string and provide a correct number of valid arguments to be interpreted correctly. Otherwise, error message will be shown.
1. `hello`- prints a welcome message
2. `all` - presents all records stored in the address book
3. `exit`, `close` - exits the CLI
5. `add <name> <phone>` - adds a new contact, if there is no such name in the address book, raises an error about duplicate contact if same name and phone are already stored, updates record with the new phone otherwise
6. `change <username> <old_phone> <new_phone>` - if the old_phone is found in the records and the new phone is valid, updates the phone number
7. `phone <username>` - lists all phone numbers stored for the user with the name, if record exists
8. `add-birthday <name> <date(DD.MM.YYYY)>` - if birthday is provided in the valid format and record exists, stores birthdays of the user
9. `show-birthday <name>` - shows birthday of user with the given name, if such contact exists
10. `birthdays` - shows birthdays of the users stored in the address book that are coming next week