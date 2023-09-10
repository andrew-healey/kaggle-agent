from termcolor import colored


def print_agent_response(agent_response,*args,**kwargs):
    """
    Print the agent response to the user
    """
    print(colored(agent_response, "green"),*args,**kwargs)

def print_system_text(system_text,*args,**kwargs):
    """
    Print the system text to the user
    """
    print(colored(system_text, "blue"),*args,**kwargs)