#!/usr/bin/env python3

import subprocess
import os
import shutil
import getpass

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
    base_muttrc_path = os.path.join(os.getcwd(), "./config/.muttrc")
    muttrc_path = os.path.join(MUTT_CONFIG_DIRECTORY, ".muttrc")
    shutil.copyfile(base_muttrc_path, muttrc_path)

    with open(base_muttrc_path, "r") as base, open(muttrc_path, "w") as updated:
        print("\nPlease enter your proton bridge credentials.")
        print("You can find them at https://protonmail.com/bridge/install\n")
        realname = input("Full name: ")
        email = input("Email address: ")
        password = getpass.getpass("Proton bridge password: ")
        smtp_port = input("Proton bridge smtp port (default 1025): ") or 1025
        smtp_url = f"smtp://{email}:{password}@localhost:{smtp_port}"

        updated.write(f'set from = "{email}"\n')
        updated.write(f'set realname = "{realname}"\n')
        updated.write(f'set imap_user = "{email}"\n')
        updated.write(f'set imap_pass = "{password}"\n')
        updated.write(f'set smtp_url = "{smtp_url}"\n')

        updated.write(base.read())

    print("The '.muttrc' file has been created successfully.")


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
