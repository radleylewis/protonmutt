#!/usr/bin/env python3

import subprocess
import os
import shutil
from getpass import getpass


MUTT_CONFIG_DIRECTORY = os.path.expanduser("~/.config/mutt")
DEPENDENCIES = {"neomutt"}


# def install_dependencies():
#     for package in DEPENDENCIES:
#         if not is_installed(package):
#             print(f"Installing {package}...")
#             subprocess.run(["sudo", "pacman", "-Syu", package], check=True)
#         else:
#             print(f"{package} is already installed. Skipping...")
#


class ProtonMutt:
    user_name: str
    user_email: str
    imap_pass: str
    smtp_pass: str
    imap_port = 1143
    smtp_port = 1025

    def _copy_file(self, dir: str, name: str) -> None:
        file_to_copy = os.path.join(os.getcwd(), f"./{dir}/{name}")
        dest_of_file = os.path.join(MUTT_CONFIG_DIRECTORY, name)
        shutil.copyfile(file_to_copy, dest_of_file)

    @property
    def _smtp_url(self) -> str:
        return f"smtp://{self.user_email}:{self.smtp_pass}@localhost:{self.smtp_port}"

    @property
    def _folder(self) -> str:
        return f"imap://localhost:{self.imap_port}"

    def create_mutt_directories(self) -> None:
        if os.path.exists(MUTT_CONFIG_DIRECTORY):
            text = (
                "The '.config/mutt' dir already exists. Do you want to proceed? (y/N): "
            )
            if input(text).lower() not in ["y", "yes"]:
                raise Exception("User canceled the process.")
        else:
            os.makedirs(MUTT_CONFIG_DIRECTORY)
            os.makedirs(MUTT_CONFIG_DIRECTORY + "/bodies")
            print("The '.config/mutt' directory has been created successfully.")

    def get_user_info(self) -> None:
        print("\nPlease enter your proton bridge credentials.\n")
        self.user_email = input("Email address: ")
        self.real_name = input("Full name: ")
        self.imap_port = input("Proton bridge imap port (defaults to 1143): ") or 1143
        self.smtp_port = input("Proton bridge smtp port (defaults to 1025): ") or 1025
        self.imap_pass = getpass("Proton imap bridge password: ")
        self.smtp_pass = getpass("Proton smtp bridge password: ")

    def create_muttrc(self) -> None:
        muttrc_path = os.path.join(os.getcwd(), "./tmp/muttrc")
        with open(muttrc_path, "w") as muttrc:
            muttrc.write(f'set realname = "{self.real_name}"\n')
            muttrc.write('set pgp_default_key = "<gpg key identifier>"\n')
            muttrc.write('source "gpg -dq ~/.config/mutt/credentials.gpg |"\n')
            muttrc.write(f'set pgp_sign_as = "{self.real_name}"\n')
            muttrc.write("set pgp_use_gpg_agent\n")

            muttrc.write(f'set from = "{self.user_email}"\n')
            muttrc.write(f'set folder = "{self._folder}"\n')
            muttrc.write(f'set spoolfile = "{self._folder}/INBOX"\n')
            muttrc.write(f'set postponed = "{self._folder}/[Protonmail]/Drafts"\n')
            muttrc.write(f'set record = "{self._folder}/[Protonmail]/Sent Mail"\n')
            muttrc.write(f'set trash = "{self._folder}/[Protonmail]/Trash"\n')
            muttrc.write(f'set mbox = "{self._folder}/[Protonmail]/All Mail"\n')
            muttrc.write('mailboxes =Starred =Drafts =Sent =Spam =Trash"\n')
            muttrc.write("source muttrc.base\n")
            muttrc.write("source muttrc.colour_scheme\n")

    def create_credentials(self) -> None:
        credentials_path = os.path.join(os.getcwd(), "./tmp/credentials")
        with open(credentials_path, "w") as credentials:
            credentials.write(f'set imap_pass = "{self.imap_pass}"\n')
            credentials.write(f'set imap_user = "{self.user_email}"\n')
            credentials.write(f'set smtp_url = "{self._smtp_url}"\n')

    def sign_credentials(self) -> None:
        os.seteuid(os.getuid())  # Temporarily change the euid to effective user ID
        subprocess.run(
            ["gpg", "--sign", "./tmp/credentials"], capture_output=True, text=True
        )
        os.seteuid(os.geteuid())  # Restore the effective user ID

    def setup_neomutt(self) -> None:
        self._copy_file("tmp", "muttrc")
        self._copy_file("tmp", "credentials.gpg")
        self._copy_file("config", "signature")
        self._copy_file("config", "muttrc.colour_scheme")
        self._copy_file("config", "muttrc.base")
        self._copy_file("config", "mailcap")

    def cleanup(self) -> None:
        shutil.rmtree(os.path.join(os.getcwd(), "./tmp"))


def is_installed(package):
    try:
        subprocess.run(["pacman", "-Q", package], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    proton_mutt = ProtonMutt()
    proton_mutt.create_mutt_directories()
    proton_mutt.get_user_info()
    proton_mutt.create_muttrc()
    proton_mutt.create_credentials()
    proton_mutt.sign_credentials()
    proton_mutt.setup_neomutt()
    proton_mutt.cleanup()
