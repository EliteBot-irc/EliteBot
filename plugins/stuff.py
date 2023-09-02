from src.plugin_base import PluginBase
from src.channel_manager import ChannelManager

class Plugin(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.channel_manager = ChannelManager()  
        
    def handle_message(self, source_nick, channel, message):
        message_parts = message.split()
        
        if message_parts[0] == '&join':
            if len(message_parts) == 1:
                self.bot._ircsend(f'JOIN {channel}')
            else:
                self.channel_manager.save_channel(message_parts[1])
                self.bot._ircsend(f'JOIN {message_parts[1]}')
                
        elif message_parts[0] == '&part':
            if len(message_parts) == 1:
                self.bot._ircsend(f'PART {channel}')
            else:
                self.channel_manager.remove_channel(message_parts[1])
                self.bot._ircsend(f'PART {message_parts[1]}')
