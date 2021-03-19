import pinhook.plugin


@pinhook.plugin.command('~say', ops=True, ops_msg='This command is reserved for bot ops!')
def say_plugin(message):
    parts = message.arg.split(" ")
    target = parts[0]
    statement = " ".join(parts[1:])
    message.privmsg(target, statement)
