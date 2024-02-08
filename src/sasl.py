# sasl.py
import base64
import logging

class SASLHandler:
    NULL_BYTE = '\x00'
    ENCODING = 'UTF-8'
    AUTHENTICATE = 'AUTHENTICATE'
    PLAIN = 'PLAIN'
    CAP_END = 'CAP END'

    def __init__(self, config, _ircsend):
        self.config = config
        self._ircsend = _ircsend
        self.validate_config()

    def validate_config(self):
        """
        Validates the configuration.
        """
        if "SASL" not in self.config or "SASLNick" not in self.config["SASL"] or "SASLPassword" not in self.config["SASL"]:
            raise KeyError("Invalid configuration. 'SASL', 'SASLNick', and 'SASLPassword' are required.")
        logging.info("Configuration validated.")

    def handle_sasl(self):
        """
        Handles SASL authentication by sending an AUTHENTICATE command.
        """
        self._ircsend(f'{self.AUTHENTICATE} {self.PLAIN}')
        logging.info("Sent AUTHENTICATE command.")

    def create_authpass(self):
        """
        Creates the authpass string and encodes it.
        """
        sasl_nick = self.config["SASL"]["SASLNick"]
        sasl_pass = self.config["SASL"]["SASLPassword"]
        authpass = f'{sasl_nick}{self.NULL_BYTE}{sasl_nick}{self.NULL_BYTE}{sasl_pass}'
        encoded_authpass = base64.b64encode(authpass.encode(self.ENCODING)).decode(self.ENCODING)
        logging.info("Created and encoded authpass.")
        return encoded_authpass

    def handle_authenticate(self, args):
        """
        Handles the AUTHENTICATE command response.

        Parameters:
        args (list): List of arguments from the AUTHENTICATE command
        """
        if args[0] == '+':
            ap_encoded = self.create_authpass()
            self._ircsend(f'{self.AUTHENTICATE} {ap_encoded}')
            logging.info("Sent encoded authpass.")

    def handle_903(self, args):
        """
        Handles the 903 command by sending a CAP END command.

        Parameters:
        args (list): List of arguments from the 903 command
        """
        self._ircsend(self.CAP_END)
        logging.info("Sent CAP END command.")
