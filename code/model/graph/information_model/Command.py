class Command:
    def exec(self, parameters):
        pass


class AnyCommand(Command):
    def exec(self, parameters, conditions):
        return set(conditions) - set(parameters)


class AllCommand(Command):
    def exec(self, parameters, conditions):
        return set(conditions) & set(parameters)
