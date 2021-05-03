from src.console_creator import *

def test_command():
	print("I am just a testing function. Nothing else.")

def arg_command(arg, arg2, other_args):
	print("You inputted :", arg, "and", arg2)
	print(other_args)

def optional_args_command(required_arg, arg1=0, arg2=1):
	required_arg = convert_type(required_arg)
	arg1 = convert_type(arg1)
	arg2 = convert_type(arg2)
	print("Required argument :", required_arg, "with type", type(required_arg))
	print("Arg 1 :", arg1, "with type", type(arg1))
	print("Arg 2 :", arg2, "with type", type(arg2))

def only_call_me_once_1():
	print("It's ok :D")
	only_call_me_once_command.description = "YOU ALREADY CALLED IT !"
	only_call_me_once_command.function_to_call = only_call_me_once_2


def only_call_me_once_2():
	print("TOLD YOU TO ONLY CALL ME ONCE !")
	only_call_me_once_command.description = "YOU FOOL !"

console = Console()

console.add_command(
	Command("test", test_command, description="A testing function.")
)
console.add_command(
	Command("arg_command", arg_command, description="A command with arguments",
		required_arguments=(
			Argument("arg", "Just some random argument"),
			Argument("arg2")
		),
	    catch_others_args=True
	)
)
console.add_command(
	Command(
		"optional_args_command", optional_args_command, description="A command with optional arguments",
		required_arguments=(
			Argument("required", "A required argument"),
		),
		optional_arguments=(
			Argument("arg1", "Just a kwarg", optional=True),
			Argument("arg2", "Another kwarg", optional=True)
		)
	)
)

only_call_me_once_command = Command(
	"only_call_me_once", only_call_me_once_1, "ONLY CALL IT ONCE !", help_args_msg=False
)
console.add_command(only_call_me_once_command)

# Generated in place
console.add_command("test_fx", lambda: print("test_fx"), description="A function to test in-place command creation.")

console.launch()
