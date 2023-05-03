from pathlib import Path
from Utilities.initialize_agents import initialize_agents
from Utilities.function_utils import Functions
from Utilities.storage_interface import StorageInterface
from Logs.logger_config import Logger

logger = Logger(name="Salience")
logger.set_level('info')

# Load Agents
storage = StorageInterface()
agents_dir = Path('Agents')
agents_list = ['task_creation_agent', 'prioritization_agent', 'execution_agent', 'salience_agent', 'status_agent']
agents = initialize_agents(agents_dir, agents_list)
locals().update(agents)

# Add a variable to set the mode
functions = Functions()
functions.set_auto_mode()
status = None

# Salience loop
while True:
    collection_list = storage.storage_utils.collection_list()
    logger.log(f"Collection List: {collection_list}", 'debug')

    functions.show_tasks('Salience')
    # quit()
    # Allow for feedback if auto mode is disabled
    status_result = functions.check_status(status)
    if status_result is not None:
        feedback = functions.check_auto_mode(status_result)
    else:
        feedback = functions.check_auto_mode()

    data = salience_agent.run_salience_agent(feedback=feedback)

    logger.log(f"Data: {data}", 'debug')

    status = status_agent.run_status_agent(data)
    # quit()



