from termcolor import colored


def print_agent_response(agent_response):
    """
    Print the agent response to the user
    """
    print(colored(agent_response, "green"))

def print_system_text(system_text):
    """
    Print the system text to the user
    """
    print(colored(system_text, "blue"))