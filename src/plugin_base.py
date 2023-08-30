class PluginBase:
    def __init__(self, bot_instance):
        """
        Constructor for the base plugin.

        :param bot_instance: Reference to the main bot instance
        """
        self.bot = bot_instance
        self.commands = {}

    def activate(self):
        """
        Called when the plugin is activated.
        Can be used for setup processes specific to the plugin.
        """
        pass

    def deactivate(self):
        """
        Called when the plugin is deactivated.
        Can be used for cleanup processes specific to the plugin.
        """
        pass

    def handle_message(self, source_nick, channel, message):
        """
        Called when a message is received.

        :param source_nick: Nickname of the user who sent the message
        :param channel: Channel where the message was sent
        :param message: Content of the message
        """
        pass

    def on_connect(self):
        """
        Called when the bot connects to the server.
        """
        pass

    def on_disconnect(self):
        """
        Called when the bot disconnects from the server.
        """
        pass

    def register_command(self, command, method):
        """
        Registers a command to a specific method.

        :param command: Command string to listen for
        :param method: Method to call when the command is received
        """
        self.commands[command] = method

    def has_command(self, command):
        """
        Checks if the plugin has a specific command registered.

        :param command: Command string to check
        :return: True if the command exists, False otherwise
        """
        return command in self.commands

    def execute_command(self, command, *args, **kwargs):
        """
        Executes a registered command.

        :param command: Command string to execute
        :param args: Positional arguments for the method
        :param kwargs: Keyword arguments for the method
        """
        if self.has_command(command):
            self.commands[command](*args, **kwargs)