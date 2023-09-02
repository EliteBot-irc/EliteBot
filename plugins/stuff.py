from src.plugin_base import PluginBase
from src.channel_manager import ChannelManager
import sys

class Plugin(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.channel_manager = ChannelManager()  
        
    def handle_message(self, source_nick, channel, message):
        message_parts = message.split()
        
        if message_parts[0] == '&join':
                self.channel_manager.save_channel(message_parts[1])
                self.bot._ircsend(f'JOIN {message_parts[1]}')
                
        elif message_parts[0] == '&part':
            if len(message_parts) == 1:
                self.bot._ircsend(f'PART {channel}')
            else:
                self.channel_manager.remove_channel(message_parts[1])
                self.bot._ircsend(f'PART {message_parts[1]}')

        elif message_parts[0] == "&quit":
            if len(message_parts) == '0':
                quit_message = 'EliteBot!'
            else:
                quit_message = message[len(message_parts[0])+1:]
            self.bot._ircsend(f'QUIT {quit_message}')
            self.bot.ircsock.close()
            self.bot.connected = False
            sys.exit()
