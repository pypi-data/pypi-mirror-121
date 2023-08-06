from typing import List, Union, Tuple
from consolebundle.ConsoleCommand import ConsoleCommand


class CommandManager:

    POSSIBLE_SEPARATORS = [":", " "]

    def __init__(self, commands: List[ConsoleCommand]):
        self.__commands = commands

    def get_possible_names(self, name_parts: list) -> list:
        return [s.join(name_parts) for s in self.POSSIBLE_SEPARATORS]

    def prefixes_same_on_separators(self, command_name: str, name_parts: list) -> Tuple[bool, Union[str, None]]:
        for s in self.POSSIBLE_SEPARATORS:
            if command_name.startswith(s.join(name_parts)):
                return True, s
        return False, None

    def get_commands(self):
        return self.__commands

    def get_by_name(self, name: str) -> ConsoleCommand:
        for command in self.__commands:
            if command.get_command() == name:
                return command

        raise Exception('No command with names in "{}" found'.format(str(name)))

    def command_prefix_only(self, name_parts: list) -> bool:
        for command in self.__commands:
            command_name = command.get_command()
            prefixes_same, sep = self.prefixes_same_on_separators(command_name, name_parts)
            if not prefixes_same:
                continue
            split_command = command_name.split(sep)
            if len(name_parts) < len(split_command):
                is_sublist = True
                for i in range(len(name_parts)):
                    if name_parts[i] != split_command[i]:
                        is_sublist = False
                        break
                if is_sublist:
                    return True
        return False
