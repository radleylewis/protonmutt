#!/usr/bin/env python3

import subprocess
import os

MUTT_CONFIG_DIRECTORY = os.path.expanduser("~/.config/mutt")
DEPENDENCIES = [
    "neomutt",
]


def install_dependencies():
    for package in DEPENDENCIES:
        if not is_installed(package):
            print(f"Installing {package}...")
            install_package(package)
        else:
            print(f"{package} is already installed. Skipping...")


def setup_mutt_directory():
    if os.path.exists(MUTT_CONFIG_DIRECTORY):
        text = "The '.config/mutt' directory already exists. Do you want to proceed? (y/N): "
        if input(text).lower() not in ["y", "yes"]:
            raise Exception("User canceled the process.")
    else:
        os.makedirs(MUTT_CONFIG_DIRECTORY)
        print("The '.config/mutt' directory has been created successfully.")


def setup_default_muttrc():
    muttrc_path = os.path.join(MUTT_CONFIG_DIRECTORY, ".muttrc")
    print(muttrc_path)
    with open(muttrc_path, "w") as muttrc_file:
        muttrc_file.write("# Add your neomutt configuration here")


def install_package(package):
    subprocess.run(["sudo", "pacman", "-Syu", package], check=True)


def is_installed(package):
    try:
        subprocess.run(["pacman", "-Q", package], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    install_dependencies()
    setup_mutt_directory()
    setup_default_muttrc()
