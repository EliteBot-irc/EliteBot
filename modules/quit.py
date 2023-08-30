from src.plugin_base import PluginBase
import sys
import time

class Plugin(PluginBase):
    def __init__(self, bot_instance):
        super().__init__(bot_instance)
        
    def handle_message(self, source_nick, channel, message):
        if message.strip() == "!quit":
            self.reply_bye(source_nick, channel)

    def reply_bye(self, source_nick, channel):
        reply = "Goodbye!"
        self.bot._ircsend(f'PRIVMSG {channel} :{reply}')
        self.bot._ircsend('QUIT :Bot is shutting down')

        # Give some time for the quit message to be processed
        time.sleep(1)

        # Close the bot's socket and mark it as disconnected
        self.bot.ircsock.close()
        self.bot.connected = False
        sys.exit()
