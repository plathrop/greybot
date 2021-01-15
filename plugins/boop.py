import pinhook.plugin

from datetime import datetime, timedelta

MIN_BOOP_INTERVAL = timedelta(seconds=30)

last_boop = datetime.utcnow()


@pinhook.plugin.listener("boop")
def boop_plugin(message):
    global last_boop
    now = datetime.utcnow()
    if message.botnick in message.text \
            and message.nick != message.botnick\
            and now - last_boop > MIN_BOOP_INTERVAL:
        last_boop = now
        return pinhook.plugin.action("beep boops")
