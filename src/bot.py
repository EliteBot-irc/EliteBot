#!/usr/bin/env python3

import socket
import ssl
import time
import json
import base64
import sys
import os
import importlib.util
from src.channel_manager import ChannelManager
from src.logger import Logger
from src.plugin_base import PluginBase
from src.sasl import handle_sasl, handle_authenticate, handle_903

class Bot:
    def __init__(self, config_file):
        self.config = self._load_config(config_file)
        self.channel_manager = ChannelManager()
        self.logger = Logger('logs/elitebot.log')
        self.connected = False
        self.ircsock = None
        self.running = True
        self.plugins = []
        self.load_plugins()

    def load_plugins(self, plugin_name=None):
        self.plugins = [p for p in self.plugins if plugin_name is None or p.__class__.__name__ != plugin_name]
        plugin_folder = "./plugins"
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py') and (plugin_name is None or filename == plugin_name + '.py'):
                filepath = os.path.join(plugin_folder, filename)
                spec = importlib.util.spec_from_file_location("module.name", filepath)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'Plugin') and issubclass(module.Plugin, PluginBase):
                    plugin_instance = module.Plugin(self)
                    self.plugins.append(plugin_instance)

    def _load_config(self, config_file):
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)
        except FileNotFoundError as e:
            self.logger.error(f'Error loading config file: {e}')
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f'Error parsing config file: {e}')
            raise
        return config

    def _decode(self, bytes):
        try: 
            text = bytes.decode('utf-8')
        except UnicodeDecodeError:
            try: 
                text = bytes.decode('latin1')
            except UnicodeDecodeError:
                try: 
                    text = bytes.decode('iso-8859-1')
                except UnicodeDecodeError:
                    text = bytes.decode('cp1252')
        return text

    def _ircsend(self, msg):
        try:
            if msg != '':
                self.logger.info(f'Sending command: {msg}')
                self.ircsock.send(bytes(f'{msg}\r\n','UTF-8'))
        except Exception as e:
            self.logger.error(f'Error sending IRC message: {e}')
            raise

    def _parse_message(self, message):
        parts = message.split()
        if not parts:
            return None, None, []
        source = parts[0][1:] if parts[0].startswith(':') else None
        command = parts[1] if source else parts[0]
        args_start = 2 if source else 1
        args = []
        trailing_arg_start = None
        for i, part in enumerate(parts[args_start:], args_start):
            if part.startswith(':'):
                trailing_arg_start = i
                break
            else:
                args.append(part)
        if trailing_arg_start is not None:
            args.append(' '.join(parts[trailing_arg_start:])[1:])
        return source, command, args

    def connect(self):
        try:
            self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ircsock.settimeout(240)

            if str(self.config['BPORT'])[:1] == '+':
                self.ircsock = ssl.wrap_socket(self.ircsock)
                port = int(self.config['BPORT'][1:])
            else:
                port = int(self.config['BPORT'])

            if 'BBINDHOST' in self.config:
                self.ircsock.bind((self.config['BBINDHOST'], 0))

            self.ircsock.connect_ex((self.config['BSERVER'], port))
            self._ircsend(f'NICK {self.config["BNICK"]}')
            self._ircsend(f'USER {self.config["BIDENT"]} * * :{self.config["BNAME"]}')
            if self.config['UseSASL']:
                self._ircsend('CAP REQ :sasl')
        except Exception as e:
            self.logger.error(f"Error establishing connection: {e}")
            self.connected = False
            return

    def start(self):
        while True:
            if not self.connected:
                try:
                    self.connect()
                    self.connected = True
                except Exception as e:
                    self.logger.error(f'Connection error: {e}')
                    time.sleep(60)
                    continue

            try:
                recvText = self.ircsock.recv(2048)
                if not recvText:
                    self.connected = False
                    continue

                ircmsg = self._decode(recvText)
                source, command, args = self._parse_message(ircmsg)
                self.logger.debug(f'Received: source: {source} | command: {command} | args: {args}')

                if command == 'PING':
                    nospoof = args[0][1:] if args[0].startswith(':') else args[0]
                    self._ircsend(f'PONG :{nospoof}')


                if command == 'CAP' and args[1] == 'ACK' and 'sasl' in args[2]:
                    handle_sasl(self.config, self._ircsend)

                elif command == 'AUTHENTICATE':
                    handle_authenticate(args, self.config, self._ircsend)

                elif command == '903':
                    handle_903(self._ircsend)

                if command == 'PRIVMSG' and args[1].startswith('\x01VERSION\x01'):
                    source_nick = source.split('!')[0]
                    self._ircsend(f'NOTICE {source_nick} :\x01VERSION EliteBot 0.1\x01')

                if command == 'PRIVMSG':
                    channel, message = args[0], args[1]
                    source_nick = source.split('!')[0]
                    if message.startswith('&'):
                        cmd, *cmd_args = message[1:].split()
                        self.handle_command(source_nick, channel, cmd, cmd_args)
                    for plugin in self.plugins:
                        plugin.handle_message(source_nick, channel, message)

                if command == '001':
                    for channel in self.channel_manager.get_channels():
                        self._ircsend(f'JOIN {channel}')

                if command == 'INVITE':
                    channel = args[1]
                    self._ircsend(f'join {channel}')
                    self.channel_manager.save_channel(channel)

                if command == 'VERSION':
                    self._ircsend('NOTICE', f'{source_nick} :I am a bot version 1.0.0')

            except socket.timeout:
                self.connected = False
                self.logger.error(f'Socket timeout.')
            except Exception as e:
                self.logger.error(f'General error: {e}')
                self.connected = False

if __name__ == '__main__':
    try:
        bot = Bot(sys.argv[1])
        bot.start()
    except KeyboardInterrupt:
        print('\nEliteBot has been stopped.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
