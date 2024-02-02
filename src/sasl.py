# sasl.py
import base64

NULL_BYTE = '\x00'
ENCODING = 'UTF-8'

def handle_sasl(config, _ircsend):
    """
    Handles SASL authentication by sending an AUTHENTICATE command.

    Parameters:
    config (dict): Configuration dictionary
    _ircsend (function): Function to send IRC commands
    """
    _ircsend('AUTHENTICATE PLAIN')

def handle_authenticate(args, config, _ircsend):
    """
    Handles the AUTHENTICATE command response.

    Parameters:
    args (list): List of arguments from the AUTHENTICATE command
    config (dict): Configuration dictionary
    _ircsend (function): Function to send IRC commands
    """
    if args[0] == '+':
        if "SASLNICK" in config and "SASLPASS" in config:
            authpass = f"{config['SASLNICK']}{NULL_BYTE}{config['SASLNICK']}{NULL_BYTE}{config['SASLPASS']}"
            ap_encoded = base64.b64encode(authpass.encode(ENCODING)).decode(ENCODING)
            _ircsend(f'AUTHENTICATE {ap_encoded}')
        else:
            raise KeyError("SASLNICK and/or SASLPASS not found in config")

def handle_903(_ircsend):
    """
    Handles the 903 command by sending a CAP END command.

    Parameters:
    _ircsend (function): Function to send IRC commands
    """
    _ircsend('CAP END')