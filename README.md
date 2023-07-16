# Protonmutt

## About

This python script automatically configures your `neomutt` for use with [Protonmail](https://proton.me/mail) on Arch systems.

## Instructions

1. Install the `protonmail-bridge`. More information on installation can be found [here](https://proton.me/mail/bridge)
2. Install `neomutt` which is available in the AUR.
3. Run the following to start the script:

```bash
git clone https://github.com/radleylewis/protonmutt.git
cd protonmutt
./install.py
```

4. Follow the input prompts

## Notes

- You can adjust the colour scheme in the `muttrc.colour_scheme` file in the config directory
- Keybindings can be viewed/changed in the `muttrc.key_bindings` file in the config directory
- Other settings can be found in the `muttrc.general_settings` fil in the config directory
- Protonmail specific configurations are dynamically generated and encrypted with `gpg`

## Resources

The following resources helped in the creation of this script and may be a useful reference:

[mutt-wizard](https://muttwizard.com) - Muttwizard is a tool that automatically sets up a neomutt-based minimal email system.
[Setting up the Mutt mail client with Protonmail](https://brian-thompson.medium.com/setting-up-the-mutt-mail-client-with-protonmail-49c042486b3) - a helpful article on getting up and running with neomutt for Protonmail

## License

GNU General Public License, Version 3, 29 June 2007
