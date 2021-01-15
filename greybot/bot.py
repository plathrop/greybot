import os
from datetime import datetime, timedelta

from pinhook.bot import Bot as PinBot


class Bot(PinBot):
    def __init__(self):
        server = "irc.canternet.org"
        port = 6697

        nickname = "greybot"
        nick_pass = os.environ.get("NICK_PASSWORD", None)
        channels = ["#Bot", "#boop_the_snoot"]

        ops = ["greytalyn"]

        self.join_times = {}

        super().__init__(channels, nickname, server,
                         port=port,
                         ssl_required=True,
                         ops=ops,
                         log_level="debug",
                         ns_pass=nick_pass,
                         cmd_prefix=':')

    def _on_join(self, connection, event):
        self.join_times[event.target] = datetime.utcnow()
        super(Bot, self)._on_join(connection, event)

    def call_internal_commands(self, channel, nick, cmd, text, arg, c):
        if channel == nick:
            return super(Bot, self).call_internal_commands(channel, nick, cmd, text, arg, c)

        if (datetime.utcnow() - self.join_times[channel]) > timedelta(seconds=15):
            # Wait 15 seconds after joining a channel before processing internal commands from that channel.
            # This allows us to avoid problems in channels that do history replay on join.
            return super(Bot, self).call_internal_commands(channel, nick, cmd, text, arg, c)
        else:
            self.logger.info("Ignoring command %s for %s; received too soon after joining.", cmd, channel)
            return None
