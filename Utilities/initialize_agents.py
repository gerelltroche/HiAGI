import os
import importlib
import sys
from contextlib import contextmanager


@contextmanager
def add_to_sys_path(path):
    sys.path.append(path)
    yield
    sys.path.remove(path)


def initialize_agents(agents_dir, agent_names=None):
    """
    Initializes agent instances from the given directory.

    The function imports and initializes agent classes from Python files
    located in the agents_dir. If a list of agent_names is provided, only
    agents with matching module names will be initialized.

    :param agents_dir: (str) The directory containing agent Python files.
    :param agent_names: (list, optional) A list of agent module names to initialize.
        If None, all agents in the directory will be initialized.
        Defaults to None.
    :return: A list of initialized agent instances.
    """
    agents = {}

    # Get all the filenames in the agents folder
    agent_files = os.listdir(agents_dir)
    print(f"agents_files {agent_files}")

    # Add the agents_dir to the sys.path
    sys.path.append(agents_dir)

    # Loop through all the files and initialize the agents
    for agent_file in agent_files:
        # Check if the file is a Python file
        if agent_file.endswith(".py"):
            # Remove the file extension to get the module name
            module_name = agent_file[:-3]
            print(f"found {module_name}")

            # Check if the user provided a list of agent names and if the current agent is in the list
            if agent_names is None or module_name in agent_names:
                # Import the agent module dynamically
                try:
                    agent_module = importlib.import_module(module_name)
                except ModuleNotFoundError:
                    capitalized_module_name = ''.join(word.title() for word in module_name.split('_'))
                    agent_module = importlib.import_module(capitalized_module_name)
                print(f"added {agent_module}")
                # Create an instance of the agent class
                try:
                    # Assuming the agent class has the same name as the module
                    agent_class = getattr(agent_module, module_name)
                except AttributeError:
                    # Try the capitalized version
                    capitalized_module_name = ''.join(word.title() for word in module_name.split('_'))
                    agent_class = getattr(agent_module, capitalized_module_name)

                agent_instance = agent_class()

                # Add the agent instance to the list of agents
                agents[module_name] = agent_instance
    print(agents)
    return agents
