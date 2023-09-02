from src.plugin_base import PluginBase

class Plugin(PluginBase):
        
    def handle_message(self, source_nick, channel, message):
        if message == '!hello':
            self.bot._ircsend(f'PRIVMSG {channel} :Hello, {source_nick}!')
