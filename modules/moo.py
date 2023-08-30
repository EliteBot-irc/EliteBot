from src.plugin_base import PluginBase

class Plugin(PluginBase):
    def __init__(self, bot_instance):
        super().__init__(bot_instance)
        
    def handle_message(self, source_nick, channel, message):
        # Check if the received message is the command !moo
        if message.strip() == "!moo":
            self.reply_moo(source_nick, channel)

    def reply_moo(self, source_nick, channel):
        reply = "Moo!"
        self.bot._ircsend(f'PRIVMSG {channel} :{reply}')
