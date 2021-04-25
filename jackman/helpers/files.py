import os
from shutil import rmtree


def get_cwd():
    """Retrieves the current working directory.

    Returns:
        str: The path to the current working directory.
    """
    return os.getcwd()


def get_jackman_dir():
    """Retrieves the path to the installation folder of the Jackman module.

    Returns:
        str: The path to the jackman module folder.
    """
    return os.path.dirname(os.path.abspath(__file__))


def set_dir(directory):
    """Changes the current directory to the specified directory.

    Args:
        directory (str): The path to the directory to change the working directory to.

    Returns:
        bool: Whether or not changing the directory was successful.
    """
    try:
        os.chdir(str(directory))
        return True
    except OSError:
        return False


def force_create_empty_directory(directory):
    """Forcefully creates an empty directory, even when it already exists.

    Args:
        directory (str): The path to the directory that needs to be created.

    Warning:
        This command always creates a new directory on the path. Only use it if you are sure that you can trust the
        function input. In all other cases, please use os.mkdir and catch the exception yourself.
    """
    try:
        os.mkdir(directory)
    except FileExistsError:
        rmtree(directory)
        os.mkdir(directory)


def cd_is_project():
    """Checks whether or not the current directory is a Jackman project.

    Returns:
        bool: Whether or not the current directory is an initialized Jackman project.
    """
    return os.path.isfile('.jackman')


def load_files(path):
    """Indexes files in a path and loads them into a dict.

    Args:
        path (str): The path to the file that should be loaded into a dict.

    Returns:
          dict: All filenames in the specified path.
    """
    files = {}
    for file in os.listdir(path):
        files[file] = os.path.relpath(file)

    return files