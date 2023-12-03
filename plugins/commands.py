from src.plugin_base import PluginBase
from src.channel_manager import ChannelManager
import sys

class Plugin(PluginBase):
        
    def handle_message(self, source_nick, channel, message):
        message_parts = message.split()
        self.channel_manager = ChannelManager()  
        if message_parts[0] == '!hello':
            self.bot._ircsend(f'PRIVMSG {channel} :Hello, {source_nick}!')
   
        elif message_parts[0] == '!join':
            self.channel_manager.save_channel(message_parts[1])
            self.bot._ircsend(f'JOIN {message_parts[1]}')

        elif message_parts[0] == '!part':
            if len(message_parts) == 1:
                self.bot._ircsend(f'PART {channel}')
                self.channel_manager.remove_channel(channel)
            else:
                self.bot._ircsend(f'PART {message_parts[1]}')
                self.channel_manager.remove_channel(message_parts[1])

        elif message_parts[0] == '!quit':
            if len(message_parts) == 1:
                quit_message = 'EliteBot!'
            else:
                quit_message = ' '.join(message_parts[1:])
            self.bot._ircsend(f'QUIT {quit_message}')
            self.bot.ircsock.close()
            self.bot.connected = False
            sys.exit()
