from model.graph.information_model.Command import *


class BaseOption:
    def __init__(self):
        self.command = Command
        self.parameters = list or None

    def exec(self):
        self.command.exec(self.parameters)


class DocOptions:
    options = dict(all=AllCommand(), any=AnyCommand())

'''
class TimeOption:
    options = dict()


class RoleOption:
    options = dict()
'''

class Option(BaseOption):
    docOptions = DocOptions().options
    #timeOptions = TimeOption().options
    #roleOptions = RoleOption().options

    #optionsDicts = [docOptions, timeOptions, roleOptions]
    optionsDicts = docOptions

    def find_command_in_dicts(self, command):
        #for optDict in self.optionsDicts:
        docOptions = DocOptions().options
        command = docOptions.get(command)
        if command:
            return command

    def __init__(self, command, args):
        finding_command = self.find_command_in_dicts(command)
        if finding_command:
            super().__init__()
            self.parameters = args
            self.command = finding_command

