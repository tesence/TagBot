import os

from tag_bot import bot as client


# pylint: disable=missing-function-docstring
def main():

    bot = client.Bot(command_prefix="?")
    bot.run(os.getenv('TAG_BOT_TOKEN'), log_handler=None)


if __name__ == '__main__':
    main()
