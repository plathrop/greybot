import faulthandler
import signal

from greybot.bot import Bot

faulthandler.enable()


def main():
    bot = Bot()
    exit_message = "Goodbye!"

    try:
        bot.start()
    except Exception as err:
        bot.logger.error(err)
    finally:
        bot.die(exit_message)


if __name__ == '__main__':
    main()

