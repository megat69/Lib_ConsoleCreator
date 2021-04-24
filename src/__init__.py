"""
Python lib that makes creating a console a simple task !
"""

class Console:
    """
    The console class, contains all the commands.
    """
    def __init__(self, pointer:str=">>>", lowercase_commands:bool=False,
                 exit_aliases:(tuple, list)=("exit", "end", "quit"), ignore_minor_errors:bool=False,
                 optional_args_prefix:str="--", end_message:(str, None)="Console closed.",
                 help_ignore_no_description:bool=False):
        """
        Every parameter is optional.
        :param pointer: The pointer that will be displayed before the input.
        :param lowercase_commands: If commands should not match the case.
        :param exit_aliases: The commands that will shutdown the console.
        :param ignore_minor_errors: Whether or not functions with no arguments should throw an exception if arguments are given.
        :param optional_args_prefix: The prefix in front of an optional argument.
        :param end_message: The message to display on console close. Can also be None, and in that case, nothing will be printed.
        :param help_ignore_no_description: Whether or not the help command should print if no description is provided for a command. Default is False.
        """
        self.commands = []
        self.is_launched = False
        self.pointer = pointer
        self.lowercase_commands = lowercase_commands
        self.exit_aliases = exit_aliases
        self.ignore_minor_errors = ignore_minor_errors
        self.optional_args_prefix = optional_args_prefix
        self.end_message = end_message
        self.help_ignore_no_description = help_ignore_no_description
        self.add_command(
            Command("help", self.help_function, description="The help command, displays this message.", help_args_msg=False)
        )

    def help_function(self):
        print("Help :")
        for command in self.commands:
            print("-", command.name, ":", command.description if command.description is not None else\
                ("No description provided." if self.help_ignore_no_description is False else ""))
            # Displaying the required args
            if command.required_arguments is None:
                if command.help_args_msg is True:
                    print("\tThis function does not require any arguments.")
            else:
                for argument in command.required_arguments:
                    print("\t" + argument.name, ":",
                          argument.description if argument.description is not None else\
                              ("No description provided." if self.help_ignore_no_description is False else ""))

            # Displaying the optional args
            if command.optional_arguments is None:
                if command.help_args_msg is True:
                    print("\tThis function does not have any optional arguments.")
            else:
                for argument in command.optional_arguments:
                    print("\t" + argument.name, ":",
                          argument.description if argument.description is not None else "No description provided")

        print("Commands to exit the console :")
        for alias in self.exit_aliases:
            print("-", alias)

    def launch(self):
        """
        Launches the console.
        """
        self.is_launched = True
        while self.is_launched is True:
            user_input = input(self.pointer + " ")
            if user_input == "":
                continue
            if user_input.lower() in self.exit_aliases:
                self.destroy()

            # Looping through the commands list to find a match
            found = False
            for command in self.commands:
                command_name = user_input.split(" ")[0] if self.lowercase_commands is False else user_input.split(" ")[0].lower()

                # If it found a match
                if (isinstance(command.name, str) and command_name == command.name) or\
                        (isinstance(command.name, (list, tuple)) and command_name in command.name):
                    # If the function does not require any arguments
                    if command.required_arguments is None and command.optional_arguments is None:
                        # If there were arguments given
                        if len(user_input.split(" ")) > 1 and self.ignore_minor_errors is False:
                            print("/!\\ This function does not require any arguments. /!\\")

                        command.function_to_call()

                    # Otherwise
                    else:
                        user_input = user_input.split(" ")[1:]
                        optional_args = {}

                        # Reuniting strings
                        for index, element in enumerate(user_input):
                            # Gets the string
                            if element.startswith("\""):
                                elements = index + 1
                                try:
                                    while not user_input[elements].endswith("\""):
                                        user_input[index] += " " + user_input[elements]
                                        elements += 1
                                except IndexError:
                                    print("The string never ends.")
                                    self.launch()
                                    return
                                user_input[index] += " " + user_input[elements]

                                for i in range(elements - index):
                                    user_input.pop(index + 1)

                                # Removing the quotes
                                user_input[index] = user_input[index][1:-1]
                                # Freeing the memory
                                del elements
                            # Getting the optional arguments
                            elif element.startswith(self.optional_args_prefix):
                                element = element.replace(self.optional_args_prefix, "", 1)

                                # Detecting if the arg value is existing
                                try:
                                    _ = user_input[index + 1]
                                except IndexError:
                                    print(f"No value has been given for the argument '{user_input[index].replace(self.optional_args_prefix, '', 1)}'")
                                    self.launch()
                                    return

                                # Getting the string
                                if user_input[index + 1].startswith("\""):
                                    elements = index + 2
                                    try:
                                        while not user_input[elements].endswith("\""):
                                            user_input[index + 1] += " " + user_input[elements]
                                            elements += 1
                                    except IndexError:
                                        print("The string never ends.")
                                        self.launch()
                                        return
                                    user_input[index + 1] += " " + user_input[elements]

                                    for i in range(elements - index - 1):
                                        user_input.pop(index + 2)

                                    # Removing the quotes
                                    user_input[index + 1] = user_input[index + 1][1:-1]
                                    # Freeing the memory
                                    del elements

                                optional_args[element] = user_input.pop(index + 1)
                                # Removing the element name
                                user_input.pop(index)

                        try:
                            # Detecting if too many args
                            if command.required_arguments is not None and\
                                    len(user_input) > len(command.required_arguments):
                                # If wanted, appending a tuple of the remaining args to the list of args
                                if command.catch_others_args is True:
                                    remaining_args = tuple(user_input[len(command.required_arguments):])
                                    user_input = user_input[:len(command.required_arguments)]
                                    user_input.append(remaining_args)
                                    del remaining_args
                                else:
                                    # If not, then we see that there are too many arguments
                                    raise TypeError

                            # Calling the function
                            # If no optional arguments exists
                            if command.optional_arguments is None or len(command.optional_arguments) == 0:
                                command.function_to_call(*user_input)
                            # If no required arguments exists, but optionals do
                            elif command.required_arguments is None or len(command.required_arguments) == 0:
                                command.function_to_call(**optional_args)
                            # If both exists
                            else:
                                command.function_to_call(*user_input, **optional_args)

                        except TypeError:
                            try:
                                print(f"This function requires {len(command.required_arguments)} arguments, got {len(user_input)}.")
                            except TypeError:
                                print(f"This function requires no arguments, got {len(user_input)}.")
                            print("This error might also come from an unknown keyword argument.\n"
                                  "See this function's help for more info.")

                    found = True
                    break

            if found is False and user_input not in self.exit_aliases and user_input != "help":
                print("Command not found. Type 'help' for the list of available commands.")

    def add_command(self, command):
        """
        Adds a command to the console.
        The most important commands should be added first.
        :param command: The command to add. Should be an instance of Command.
        """
        # If the console is already launched, we stop the ability to use this function.
        if self.is_launched: raise Exception("Console is already launched, cannot add any more commands.")
        # If it is not a command
        if not isinstance(command, Command): raise Exception("Command must be an instance of Command().")

        # Checking if a command with the same name already exists
        # If so, returning an error
        for registered_command in self.commands:
            if registered_command.name == command.name:
                raise Exception(f"Command '{command.name}' already exists")

        # Registering the command
        self.commands.append(command)

    def destroy(self):
        if self.end_message is not None: print(self.end_message)
        self.is_launched = False

class Command:
    """
    Creates a new console command.
    """
    def __init__(self, name:(str, list, tuple), function_to_call, description:str=None,
                 required_arguments:(tuple, list)=None, optional_arguments:(tuple, list)=None,
                 catch_others_args:bool=False, help_args_msg:bool=True):
        """
        :param name: A string that defines the name of the command. Should not contain any space.
        :param function_to_call: The function to call on command output.
        :param description: (Optional) The description of the command.
        :param required_arguments: (Optional) The arguments required for the command. These have to be instances of Argument class.
        :param optional_arguments: (Optional) The optional arguments required for the command.
        :param catch_others_args: (Optional) Whether or not to return all the args inputted by the user as a tuple
        :param help_args_msg: (Optional) Whether or not the help command should print that the command does not have any arguments. True by default.
        """
        # Raising an exception if a space is in the name
        if isinstance(name, str) and " " in name:
            raise Exception("Command name should not contain any spaces.")
        elif isinstance(name, (list, tuple)):
            for element in name:
                if " " in element:
                    raise Exception("Command name should not contain any spaces.")

        self.name = name
        self.description = description
        self.required_arguments = tuple(required_arguments) if isinstance(required_arguments, list) else required_arguments
        self.optional_arguments = tuple(optional_arguments) if isinstance(optional_arguments, list) else optional_arguments
        self.function_to_call = function_to_call
        self.catch_others_args = catch_others_args
        self.help_args_msg = help_args_msg

class Argument:
    """
    Creates an argument for the commands.
    """
    def __init__(self, name:str, description:str=None, optional:bool=False):
        """
        :param name: The argument name.
        :param description: (Optional) The argument description.
        :param optional: (Optional) If the argument is optional.
        """
        self.name = name
        self.description = description
        self.optional = optional

def convert_type(variable):
    """
    Automatically converts the type of the inputted variable to the type that suits it the most.
    :param variable: The variable needing its type to be converted.
    :return: The variable, with its new type.
    """
    # Booleans/NoneType check
    if str(variable).lower() == "none":
        return None
    elif str(variable).lower() == "true":
        return True
    elif str(variable).lower() == "false":
        return False

    try:
        variable = int(variable)
    except ValueError:
        try:
            variable = float(variable)
        except ValueError:
            pass

    return variable
