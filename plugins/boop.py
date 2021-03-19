import pinhook.plugin

from datetime import datetime, timedelta, timezone

MIN_BOOP_INTERVAL = timedelta(seconds=30)


@pinhook.plugin.listener("boop")
def boop_plugin(message):
    boop_key = "last_boop.{}".format(message.channel)
    now = datetime.now(timezone.utc)
    last_boop = message.bot.datastore.get(boop_key)

    if last_boop is None:
        last_boop = now - timedelta(days=1)
    else:
        last_boop = datetime.fromisoformat(last_boop)

    if message.botnick in message.text \
            and message.nick != message.botnick\
            and now - last_boop > MIN_BOOP_INTERVAL:
        message.bot.datastore.set(boop_key, now.isoformat())
        return pinhook.plugin.action("beep boops")
