

def handle_ping(bot, args):
    """
    Handle PING command from the server.
    """
    nospoof = args[0][1:] if args[0].startswith(':') else args[0]
    bot._ircsend(f'PONG :{nospoof}')

def handle_cap(bot, args):
    """
    Handle CAP command from the server.
    """
    if args[1] == 'ACK' and 'sasl' in args[2]:
        bot.sasl_handler.handle_sasl()

def handle_authenticate(bot, args):
    """
    Handle AUTHENTICATE command from the server.
    """
    bot.sasl_handler.handle_authenticate(args)

def handle_903(bot, args):
    bot.sasl_handler.handle_903(bot._ircsend)

def handle_privmsg(bot, args):
    source, args = args
    if args[1].startswith('\x01VERSION\x01'):
        source_nick = source.split('!')[0]
        bot._ircsend(f'NOTICE {source_nick} :\x01VERSION EliteBot 0.1\x01')
    else:
        channel, message = args[0], args[1]
        source_nick = source.split('!')[0]
        if message.startswith('&'):
            cmd, *cmd_args = message[1:].split()
            bot.handle_command(source_nick, channel, cmd, cmd_args)
        for plugin in bot.plugins:
            plugin.handle_message(source_nick, channel, message)

def handle_001(bot, args):
    for channel in bot.channel_manager.get_channels():
        bot._ircsend(f'JOIN {channel}')

def handle_invite(bot, args):
    channel = args[1]
    bot._ircsend(f'join {channel}')
    bot.channel_manager.save_channel(channel)

def handle_version(bot, source):
    source_nick = source.split('!')[0]
    bot._ircsend('NOTICE', f'{source_nick} :I am a bot version 1.0.0')