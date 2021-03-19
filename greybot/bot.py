import os
from datetime import datetime, timedelta, timezone

import redis
from pinhook.bot import Bot as PinBot


class Bot(PinBot):
    def __init__(self):
        server = "irc.canternet.org"
        port = 6697

        nickname = "greybot"
        nick_pass = os.environ.get("NICK_PASSWORD", None)
        channels = ["#Bot", "#boop_the_snoot"]

        ops = ["greytalyn"]

        self.datastore = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True)

        super().__init__(channels, nickname, server,
                         port=port,
                         ssl_required=True,
                         ops=ops,
                         log_level="debug",
                         ns_pass=nick_pass,
                         cmd_prefix=':')

    @staticmethod
    def _join_key(channel):
        return "join.{}".format(channel)

    def _on_join(self, connection, event):
        join_key = self._join_key(event.target)
        now = datetime.now(timezone.utc)
        self.datastore.set(join_key, now.isoformat())
        self.send_join_message(event.target)
        super(Bot, self)._on_join(connection, event)

    def send_join_message(self, channel):
        messages_key = "join_message.{}".format(channel)
        message = self.datastore.srandmember(messages_key)
        if message is not None:
            self.connection.privmsg(channel, message)

    def get_join_time(self, channel):
        key = self._join_key(channel)
        return datetime.fromisoformat(self.datastore.get(key))

    def call_internal_commands(self, channel, nick, cmd, text, arg, c):
        if channel == nick:
            return super(Bot, self).call_internal_commands(channel, nick, cmd, text, arg, c)

        # I don't love that this is running a redis query on every message but YOLO for now.
        if (datetime.now(timezone.utc) - self.get_join_time(channel)) > timedelta(seconds=15):
            # Wait 15 seconds after joining a channel before processing internal commands from that channel.
            # This allows us to avoid problems in channels that do history replay on join.
            return super(Bot, self).call_internal_commands(channel, nick, cmd, text, arg, c)
        else:
            self.logger.info("Ignoring command %s for %s; received too soon after joining.", cmd, channel)
            return None
