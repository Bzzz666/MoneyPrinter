import os

from termcolor import colored

def clean_dir(path: str) -> None:
    """
    Removes every file in a directory

    Args:
        path (str): Path to directory

    Returns:
        None
    """

    for file in os.listdir(path):
        os.remove(os.path.join(path, file))
    
    print(colored(f"[+] Cleaned {path} directory", "green"))