import asyncio
import logging

from hikcamerabot.setup import BotSetup
from hikcamerabot.version import __version__


class BotLauncher:
    """Bot launcher which parses configuration file, creates bot with
    camera instances and finally starts the bot.
    """

    def __init__(self) -> None:
        """Constructor."""
        self._log = logging.getLogger(self.__class__.__name__)
        self._setup = BotSetup()
        self._bot = self._setup.get_bot()

    async def launch(self) -> None:
        """Launch (run) bot."""
        await self._start_bot()

    async def _start_bot(self) -> None:
        """Start telegram bot and related processes."""
        await self._bot.start()

        self._log.info('Starting %s bot version %s',
                       (await self._bot.get_me()).first_name, __version__)

        self._bot.start_tasks()
        await self._bot.send_startup_message()
        await self._run_bot_forever()

    async def _run_bot_forever(self) -> None:
        while True:
            await asyncio.sleep(86400)
