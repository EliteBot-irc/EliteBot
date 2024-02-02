# sasl.py
import base64

def handle_sasl(config, _ircsend):
    _ircsend('AUTHENTICATE PLAIN')

def handle_authenticate(args, config, _ircsend):
    if args[0] == '+':
        authpass = config["SASLNICK"] + '\x00' + config["SASLNICK"] + '\x00' + config["SASLPASS"]
        ap_encoded = str(base64.b64encode(authpass.encode('UTF-8')), 'UTF-8')
        _ircsend('AUTHENTICATE ' + ap_encoded)

def handle_903(_ircsend):
    _ircsend('CAP END')