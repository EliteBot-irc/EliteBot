from src.plugin_base import PluginBase
from src.channel_manager import ChannelManager
import sys
import time

class Plugin(PluginBase):
        
    def handle_message(self, source_nick, channel, message):
        message_parts = message.split()
        self.channel_manager = ChannelManager()  
        if message_parts[0] == '!hello':
            self.bot._ircsend(f'PRIVMSG {channel} :Hello, {source_nick}!')
   
        elif message_parts[0] == '!join':
            if len(message_parts) == 0:
                self.bot._ircsend(f'PRIVMSG {channel} :Please specify a channel to join')
                return
            else:
                self.channel_manager.save_channel(message_parts[1])
                self.bot._ircsend(f'JOIN {message_parts[1]}')

        elif message_parts[0] == '!part':
            if len(message_parts) == 1:
                self.bot._ircsend(f'PART {channel}')
                self.channel_manager.remove_channel(channel)
            else:
                self.bot._ircsend(f'PART {message_parts[1]}')
                self.channel_manager.remove_channel(message_parts[1])


        elif message_parts[0] == "!quit":
            if len(message_parts) == 0:
                quit_message = 'EliteBot!'
            else:
                quit_message = message[len(message_parts[0])+1:]
            self.bot._ircsend(f'QUIT :{quit_message}')
            self.bot.ircsock.close()
            self.bot.connected = False
            sys.exit()

        elif message_parts[0] == "!raw":
            if len(message_parts) > 1:
                if message_parts[1].upper() == "PRIVMSG" and len(message_parts) > 3:
                    raw_command = ' '.join(message_parts[1:3]) + " :" + ' '.join(message_parts[3:])
                else:
                    raw_command = ' '.join(message_parts[1:])
                self.bot._ircsend(raw_command)