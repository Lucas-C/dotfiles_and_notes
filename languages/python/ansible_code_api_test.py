#!/usr/bin/env python3

# Starting points:
# * Learning test 1
#   - files: hosts ansible.cfg
#   - command: ansible -i hosts -m ping all
# * Learning test 2
#   - files: hosts ansible.cfg poll_test.yaml
#   - command: ansible-playbook -i hosts poll_test.yaml
#   - same through Python API:

# This must be configured before other ansible imports:
from ansible.utils.display import Display
display = Display()  # this variable name is an ansible convention and is imported from ansible code with `from __main__ import display`
display.verbosity = 3

from ansible import constants as C
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_executor import PlaybookExecutor


playbook_filepath = 'poll_test.yaml'
hosts_filepath = 'hosts'

loader = DataLoader()
inventory = InventoryManager(loader=loader, sources=hosts_filepath)
variable_manager = VariableManager(loader=loader, inventory=inventory)

from argparse import Namespace
options = Namespace(listhosts=None, listtasks=None, listtags=None, syntax=None, module_path=None,
                    become=None, become_method=C.DEFAULT_BECOME_METHOD, become_user=C.DEFAULT_BECOME_USER,
                    check=False, diff=C.DIFF_ALWAYS, forks=C.DEFAULT_FORKS, connection=C.DEFAULT_TRANSPORT)

pbex = PlaybookExecutor(playbooks=[playbook_filepath], inventory=inventory, variable_manager=variable_manager, loader=loader,
                        options=options, passwords={})
results = pbex.run()
print(results)
