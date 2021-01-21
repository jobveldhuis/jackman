import logging
from pkg_resources import iter_entry_points, get_distribution
from sys import argv
from tabulate import tabulate

from jackman.helpers import setup_logging, cd_is_project, get_cwd


setup_logging()
log = logging.getLogger(__name__)
registered_commands = {}
for entry_point in iter_entry_points('jackman.commands'):
    if entry_point.name not in registered_commands.keys():
        try:
            registered_commands[entry_point.name] = entry_point.load()
            log.debug(f'Found and successfully added {entry_point.name}')
        except Exception as e:
            log.exception(e, exc_info=False)
    else:
        log.debug(f'{entry_point.name} was already loaded by another source.')


def main():
    if len(argv) > 1:
        execute(argv)
    else:
        show_help()


def execute(argument_vector):
    command = argument_vector[1]
    try:
        executable_command = registered_commands[command]
        if not cd_is_project() and command not in ['create', 'help']:
            log.critical(f'Your current directory ({get_cwd()}) is not considered a valid Jackman project.')
        else:
            executable_command()
    except KeyError:
        if command in ['help', '--help', '-h']:
            show_help(argument_vector[2:])
        else:
            log.critical(f'Could not execute. "{command}" is not recognized as a valid Jackman command.')


def show_help(specified_command=None):
    if not specified_command:
        command_list = []
        for command in registered_commands:
            try:
                command_list.append((command, registered_commands[command].__doc__.splitlines()[0]))
            except AttributeError:
                command_list.append((command, ''))

        # TODO: Reserve help as command
        if 'help' not in command_list:
            command_list.append(('help', 'Shows this information prompt'))

        print('')
        print(f'There are {len(command_list)} commands available.')
        print('')
        print(tabulate(command_list, tablefmt='plain'))
        print('')
        print('For specific information about a command, run "jackman help <command_name>"')
        print('')
        print(f'Jackman v{get_distribution("jackman").version}')
        print('')
    else:
        if len(specified_command) > 1:
            log.error('The specified command is too long. Please enter only one command: jackman help <command>')
        elif specified_command[0] not in registered_commands:
            log.error(f'The specified command {specified_command[0]} is not recognized as a Jackman command.')
        else:
            print('')
            print(f'Showing documentation for {specified_command[0]}')
            print('')
            print(registered_commands[specified_command[0]].__doc__)
