
class InvalidCommand(Exception):
    '''raised when invalid commdand was entered by the user'''

    def __init__(self, command: str = '', *args: object) -> None:
        super().__init__(*args)
        self.command = command


class ValueNotFound(Exception):
    '''raised when value wasn't found'''

    def __init__(self, phone: str = '', name: str = '', *args: object) -> None:
        super().__init__(*args)
        self.phone = phone
        self.name = name


class DuplicateEntry(Exception):
    '''raised when same contact was added more than once'''

    def __init__(self, name: str, phone: str, *args: object) -> None:
        super().__init__(*args)
        self.name = name
        self.phone = phone


