# Console Creator
Python lib that makes creating a console a simple task !

This lib enables you to create a console where the user can input commands, with features such as command aliases, automatic help generation, and much, much more !

## Install
### Install from PyPI
To install the library, just type `pip install python-console-creator` and this should be ok.

Visit [PyPI](https://pypi.org/project/python-console-creator/) for more info.

### Install from source
Just download the file at [this link](https://github.com/megat69/Lib_ConsoleCreator/blob/main/src/console_creator/__init__.py), and import it in your project.

## Usage
*See [examples](https://github.com/megat69/Lib_ConsoleCreator/tree/main/examples) if wanted.*

This library provides multiple classes.
### The `Console` class
This class is the main console.

**How to use it ?**<br/>
Simply store it in a variable like so :
```python
from console_creator import *

console = Console()
```

While constructing the class, you can pass in some of the following parameters (all optionals) :
- `pointer` : A string containing the element that will tell the user that he should input a command. By default, `>>>`.
- `lowercase_commands` : A boolean that indicates whether or not commands should match the case. E.g. if False *(by default)* `test` and `TEST` won't be the same command. Otherwise, they will be the same.
- `exit_aliases` : A tuple or list of strings containing the name of the commands that should let the user quit the console. By default, `exit`, `end`, and `quit`.
- `ignore_minor_errors` : A boolean that indicates whether or not functions with no arguments should throw an exception if arguments are given. By default, False.
- `optional_args_prefix` : The prefix in front of an optional argument. By default, `--`.
- `end_message` : The message to display on console close. Can also be None, and in that case, nothing will be printed. By default, "`Console closed.`"
- `help_ignore_no_description` : Boolean indicating whether or not the help command should print if no description is provided for a command. Default is False.

This class contains a few methods that will help you create your commands.

#### The `launch` method
This method will launch the console.

**/!\ Beware ! After this method is called, it is no longer possible to add commands ! /!\**

#### The `destroy` method
This method will destroy the console.

Past this point, you can add commands again or launch the console again.

#### The `add_command` method
The main method of the `Console` class.

This method allows you to add new commands to the console.

*The most important commands should be added first, as they will be checked in the order in which they have been added.<br/>The later you add a command, the further it is situated in the commands list, the longest it takes. (It is just a matter of milliseconds, still)*

**/!\ An exception will be raised if you try to create two commands with the same name. /!\ **

This method takes as argument an instance of the `Command` class, which is described just below.<br/>
Otherwise, a command will be created in place, but will no longer be capable of being modified.<br/>
This method, even though is working and will be maintained, is not recommended.

### The `Command` class
This class is the class that composes a command.

It takes in as required positional arguments :
- `name` : A string that defines the name of the command. Should not contain any space, otherwise an exception will be raised.
- `function_to_call` : A callback function to call when the command is triggered.

It can take as non-required keyword arguments the following statements :
- `description` : A short description of the function, for the help command.
- `catch_others_args` : A boolean indicating whether or not to return all the args inputted by the user as a tuple. False by default.
- `help_args_msg` : Whether or not the help command should print that the command does not have any arguments if this is the case. True by default.

It can finally take two other keyword arguments : `required_arguments` and `optional_arguments`.

These arguments are a tuple or a list of instances of the `Argument` class *(see below)*, and for the `optional_arguments`, each instance should have its parameter `optional` set to `True`.

The callback function defined above should take each of the `required_arguments` as positional arguments, each of the `optional_arguments` as optional arguments, and another positional argument if the parameter `catch_others_args` is set to `True`.

### The `Argument` class
This class requires one argument : `name`, a string containing the name of the argument. This will mainly be used for the help command if the argument is required.

The class also provides two "optional" arguments *(although I recommend you to fill them)* :
- `description` : A short description of the argument, for the help command.
- `optional` : A boolean that indicates whether the argument is required or not. **THIS PARAMETER ABSOLUTELY REQUIRES TO BE SET TO `True` IF THE ARGUMENT IS OPTIONAL !**

### The `convert_type` function
As the commands inputted by the user always returns strings, I left you this function to convert a variable to the type that fits it the most among `None`, `bool`, `int`, `float`, and `string`.<br/>*(The types will be tested in that order)*

## Examples
Here are some examples of consoles, from simple to more advanced.

### Example 1 : A console with only a help command and a way to exit
I mean, why not ?

You just need to import the library, create an instance of `Console`, and launch it.

```python
from console_creator import *

console = Console()
console.launch()
```

Let's say we want this console to be only left if the user types the command `leave`, where the case of the commands doesn't count, and where no end message is printed when the console is closed.

The code should now look this way :
```python
from console_creator import *

console = Console(exit_aliases=("leave",), lowercase_commands=True, end_message=None)
console.launch()
```

### Example 2 : A console containing only a command printing "Hello World !"
To do so, we need to create a function with no arguments, and to add a command in the console.

```python
from console_creator import *

# We create the hello world function here
def hello_world_function():
  print("Hello World !")

# We create the console
console = Console()

# We add the hello-world command
console.add_command(
  #           name        callback function
  Command("hello-world", hello_world_function)
)

# We launch the console
console.launch()
```

But this one does not feature an explicit description for users who need it, so let's add one !

Just replace the line 13 with this line :
```python
Command("hello-world", hello_world_function, description="Don't look at me, I just say \"Hello World !\" :D")
```

### Example 3 : A 'hello' command, that says hello to the user with his given name
Here, we will need to add a required argument that will be the `name` of the user.
```python
from console_creator import *

# We create the hello function here
def hello_function(name):
  print(f"Hello, {name} !")

# We create the console
console = Console()

# We add the hello command
console.add_command(
  Command("hello", hello_function, description="This commands says hello to the best user in the world ;)", required_arguments=(
    Argument("name", description="Well, your name xD"),
  ))
)

# We launch the console
console.launch()
```

If you do `hello <your name>`, it should respond `Hello, <your name> !`, and that without any effort, and a clean code.

### Example 4 : The same example as above, but this time the `name` argument is not required
Let's take the code from the last example, and remake a few lines.
```python
from console_creator import *

# We create the hello function here
# The 'name' argument is set to None by default
def hello_function(name=None):
  # If name is none, we just print 'Hello !', otherwise we also print the user's name
  if name is None:
    print("Hello !")
  else:
    print(f"Hello, {name} !")

# We create the console
console = Console()

# We add the hello command
# This time, we change 'required_arguments' to 'optional_arguments', and we switch the Argument 'optional' parameter to 'True'
console.add_command(
  Command("hello", hello_function, description="This commands says hello to the best user in the world ;)", optional_arguments=(
    Argument("name", description="Well, your name xD", optional=True),
  ))
)

# We launch the console
console.launch()
```
I let you try it yourself.

### Example 5 : Let's combine both !
Let's create a command to send a message (required arg) to the user, which can be signed or anonymous (by default).
```python
from console_creator import *

# We create the function here :
def send_message_function(message, signature = "This message was anonymous"):
  print(message)
  print(signature + ".")

# We create the console
console = Console()

# We add the command
console.add_command(
  Command("send-message", send_message_function, description="This send your lovely message to the user", 
  required_arguments=(
    Argument("message", description="Your message to the user"),
  ),
  optional_arguments=(
    Argument("signature", description="Your name, or leave it blank to be anonymous.", optional=True),
  ))
)

# We launch the console
console.launch()
```

If you input `send-message "I love you, my friend." David`, you should receive in the console the following message :
```
I love you, my friend.
David.
```
Now, if you input this instead `You've been hacked !` *(so the second arg is not filled)*, you should get this :
```
You've been hacked !
This message was anonymous.
```

### Example 6 : Keeping the commands in variables to be able to change them
I'll just leave the code, try for yourself, and have fun understanding it ;)
```python
from console_creator import *

def only_call_me_once_1():
	print("It's ok :D")
	only_call_me_once_command.description = "YOU ALREADY CALLED IT !"
	only_call_me_once_command.function_to_call = only_call_me_once_2


def only_call_me_once_2():
	print("TOLD YOU TO ONLY CALL ME ONCE !")
	only_call_me_once_command.description = "YOU FOOL !"

console = Console()

only_call_me_once_command = Command(
	"only_call_me_once", only_call_me_once_1, "ONLY CALL IT ONCE !", help_args_msg=False
)
console.add_command(only_call_me_once_command)

console.launch()
```

## In Conclusion
I hope you like this library as much as I do !

I've put some effort in making it, so I would love to hear your thoughts and comments about it on my [Discord server](https://discord.gg/MBuKcUn).

If you find any bug, or are not sure about something, just post it on the Discord or [open an issue](https://github.com/megat69/Lib_ConsoleCreator/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc).