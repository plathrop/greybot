from datetime import datetime, timedelta, timezone

import pinhook.plugin


def nick_key(message):
    return "{}.{}".format(message.channel, message.nick)

def greetings_key(message):
    return "greetings.messages.{}".format(nick_key(message))

@pinhook.plugin.listener("greetings")
def greetings_plugin(message):
    greetings_interval = timedelta(minutes=30)

    last_seen_key = "greetings.last_seen.{}".format(nick_key(message))
    channel_greetings_key = "greetings.messages.{}".format(message.channel)

    now = datetime.now(timezone.utc)

    last_seen = message.bot.datastore.getset(last_seen_key, now.isoformat())
    if last_seen is not None:
        last_seen = datetime.fromisoformat(last_seen)
    else:
        last_seen = datetime.now(timezone.utc) - timedelta(days=1)

    if (now - last_seen) < greetings_interval:
        # Too soon to say anything
        return

    greeting = message.bot.datastore.srandmember(greetings_key(message))
    if greeting is None:
        greeting = message.bot.datastore.srandmember(channel_greetings_key)

    if greeting is not None:
        return pinhook.plugin.message(greeting)

@pinhook.plugin.command('~add-greeting', help_text='Add a personalized greeting.')
def add_greeting_plugin(message):
    if datetime.now(timezone.utc) - message.bot.get_join_time(message.channel) > timedelta(seconds=15):
        message.bot.datastore.sadd(greetings_key(message), message.arg)
        return pinhook.plugin.action("whirrs and buzzes as he records the new greeting")
