import pinhook.plugin


@pinhook.plugin.command('~quit', ops=True, ops_msg='This command can only be run by a bot op!')
def quit_plugin(message):
    message.bot.die("Killing myself, master {}!".format(message.nick))


@pinhook.plugin.command('~say', ops=True, ops_msg='This command is reserved for bot ops!')
def say_plugin(message):
    parts = message.arg.split(" ")
    target = parts[0]
    statement = " ".join(parts[1:])
    message.privmsg(target, statement)
