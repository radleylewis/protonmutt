#!/usr/bin/env python3

import subprocess
import os
import shutil
from getpass import getpass


MUTT_CONFIG_DIRECTORY = os.path.expanduser("~/.mutt")
REQUIRED_DEPENDENCIES = {"neomutt"}


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

    def _move_file(self, dir: str, name: str) -> None:
        file_to_copy = os.path.join(os.getcwd(), f"./{dir}/{name}")
        dest_of_file = os.path.join(MUTT_CONFIG_DIRECTORY, name)
        shutil.move(file_to_copy, dest_of_file)

    @property
    def _smtp_url(self) -> str:
        return f"smtp://{self.user_email}:{self.smtp_pass}@localhost:{self.smtp_port}"

    @property
    def _folder(self) -> str:
        return f"imap://localhost:{self.imap_port}"

    def check_dependencies(self) -> None:
        for package in REQUIRED_DEPENDENCIES:
            if not is_installed(package):
                print(f"Installing {package}...")
                subprocess.run(["sudo", "pacman", "-Syu", package], check=True)
            else:
                print(f"{package} is already installed. Skipping...")

    def create_tmp_directory(self) -> None:
        if os.path.exists("./tmp"):
            shutil.rmtree("./tmp")
        else:
            os.makedirs("./tmp")

    def create_mutt_directories(self) -> None:
        if os.path.exists(MUTT_CONFIG_DIRECTORY):
            text = "The '.mutt' dir already exists. Do you want to proceed? (y/N): "
            if input(text).lower() not in ["y", "yes"]:
                raise Exception("User canceled the process.")
        else:
            os.makedirs(MUTT_CONFIG_DIRECTORY)
            os.makedirs(MUTT_CONFIG_DIRECTORY + "/bodies")
            print("The './mutt' directory has been created successfully.")

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
            muttrc.write('source "gpg -dq ~/.mutt/protonmail.gpg |"\n')
            muttrc.write(f'set pgp_sign_as = "{self.real_name}"\n')
            muttrc.write("set pgp_use_gpg_agent\n")
            muttrc.write(f'set from = "{self.user_email}"\n')
            muttrc.write('mailboxes =Starred =Drafts =Sent =Spam =Trash"\n')
            muttrc.write("set mailcap_path = $HOME/.mutt/mailcap\n")
            muttrc.write("source muttrc.general_settings\n")
            muttrc.write("source muttrc.key_bindings\n")
            muttrc.write("source muttrc.colour_scheme\n")

    def setup_protonmail(self) -> None:
        protonmail_path = os.path.join(os.getcwd(), "./tmp/protonmail")
        with open(protonmail_path, "w") as protonmail:
            protonmail.write("set ssl_starttls = yes\n")
            protonmail.write("set ssl_force_tls = yes\n")
            protonmail.write('set send_charset = "us-ascii:utf-8"\n')
            protonmail.write(f'set imap_pass = "{self.imap_pass}"\n')
            protonmail.write(f'set imap_user = "{self.user_email}"\n')
            protonmail.write(f'set smtp_url = "{self._smtp_url}"\n')
            protonmail.write(f'set folder = "{self._folder}"\n')
            protonmail.write(f'set folder = "{self._folder}"\n')
            protonmail.write(f'set spoolfile = "{self._folder}/INBOX"\n')
            protonmail.write(f'set postponed = "{self._folder}/[Protonmail]/Drafts"\n')
            protonmail.write(f'set record = "{self._folder}/[Protonmail]/Sent Mail"\n')
            protonmail.write(f'set trash = "{self._folder}/[Protonmail]/Trash"\n')
            protonmail.write(f'set mbox = "{self._folder}/[Protonmail]/All Mail"\n')
            protonmail.write('set header_cache = "~/.mutt/cache/headers"\n')
            protonmail.write('set message_cachedir = "~/.mutt/cache/bodies"\n')
            protonmail.write('set certificate_file = "~/.mutt/certificates"\n')
            protonmail.write('set smtp_authenticators = "gssapi:login"\n')
            protonmail.write("set imap_keepalive = 900\n")
            protonmail.write(f'set from = "{self.user_email}"\n')
            protonmail.write(f'set realname = "{self.real_name}"\n')
            protonmail.write("set use_from = yes\n")
            protonmail.write("unset use_domain\n")

    def sign_protonmail(self) -> None:
        os.seteuid(os.getuid())  # Temporarily change the euid to effective user ID
        subprocess.run(
            ["gpg", "--sign", "./tmp/protonmail"], capture_output=True, text=True
        )
        os.seteuid(os.geteuid())  # Restore the effective user ID

    def setup_neomutt(self) -> None:
        self._move_file("tmp", "muttrc")
        self._move_file("tmp", "protonmail.gpg")
        self._copy_file("config", "signature")
        self._copy_file("config", "muttrc.colour_scheme")
        self._copy_file("config", "muttrc.key_bindings")
        self._copy_file("config", "muttrc.general_settings")
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
    proton_mutt.check_dependencies()
    proton_mutt.create_tmp_directory()
    proton_mutt.create_mutt_directories()
    proton_mutt.get_user_info()
    proton_mutt.create_muttrc()
    proton_mutt.setup_protonmail()
    proton_mutt.sign_protonmail()
    proton_mutt.setup_neomutt()
    proton_mutt.cleanup()
