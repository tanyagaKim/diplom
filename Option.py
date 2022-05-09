class Option:
    def __init__(self):
        self.command = None
        self.parameters = list or None

    def action(self):
        return self.command(self.parameters)


class DocOption(Option):
    def __init__(self, command, parameters):
        super().__init__()
        self.parameters = parameters

        if command == "/all":
            self.command = self.all
        elif command == "/any":
            self.command = self.any

    def all(self):
        print(self.parameters)

    def any(self):
        print(self.parameters)


class TimeOption(Option):
    pass


class RoleOption(Option):
    pass

