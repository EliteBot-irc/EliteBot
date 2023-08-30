from src.plugin_base import PluginBase

class Plugin(PluginBase):
    def __init__(self, bot_instance):
        super().__init__(bot_instance)
        self.register_command("!hello", self.say_hello)
        
    def say_hello(self, source_nick, channel, message):
        self.bot._ircsend(f'PRIVMSG {channel or source_nick} :Hello!')
