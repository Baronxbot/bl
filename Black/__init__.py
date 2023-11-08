
import os
from logging import getLogger

from telethon import TelegramClient
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged

from config import *

logging.basicConfig(level=logging.INFO, format="%(name)s - [%(levelname)s] - %(message)s")

LOGS = getLogger("Kynan-Anjay")


class nan(TelegramClient):
    def __init__(
        self, api_id=None, api_hash=None, bot_token=None,
        connection=ConnectionTcpAbridged, auto_reconnect=True, connection_retries=None, db=None, logger: Logger = LOGS, log_attempt=True, exit_on_error=True, *args, **kwargs):
        self._cache = {}
        self._dialogs = []
        self._handle_error = exit_on_error
        self._log_at = log_attempt
        self.logger = logger
        self.db = db
        kwargs["api_id"] = api_id or API_ID
        kwargs["api_hash"] = api_hash or API_HASH
        kwargs["base_logger"] = TelethonLogger
        super().__init__(**kwargs)
        self.run_in_loop(self.start_client(bot_token=bot_token))


    async def start_client(self, **kwargs):
        """function to start client"""
        if self._log_at:
            self.logger.info("Trying to login.")
        try:
            await self.start(**kwargs)
        except ApiIdInvalidError:
            self.logger.critical("API ID and API_HASH combination does not match!")
            sys.exit()
        
        except (AccessTokenExpiredError, AccessTokenInvalidError):
            self.logger.critical(
                "Bot token is expired or invalid. Create new from @Botfather and add in BOT_TOKEN env variable!"
            )
            sys.exit()
            
        self.me = await self.get_me()
        if self.me.bot:
            me = f"@{self.me.username}"
        else:
            setattr(self.me, "phone", None)
            me = self.full_name
        if self._log_at:
            self.logger.info(f"Logged in as {me}")

    def run_in_loop(self, function):
        """run inside asyncio loop"""
        return self.loop.run_until_complete(function)

    def run(self):
        """run asyncio loop"""
        self.run_until_disconnected()

    def add_handler(self, func, *args, **kwargs):
        """Add new event handler, ignoring if exists"""
        if func in [_[0] for _ in self.list_event_handlers()]:
            return
        self.add_event_handler(func, *args, **kwargs)

    @property
    def utils(self):
        return telethon_utils

    @property
    def full_name(self):
        """full name of Client"""
        return self.utils.get_display_name(self.me)

    @property
    def uid(self):
        """Client's user id"""
        return self.me.id

    def to_dict(self):
        return dict(inspect.getmembers(self))

    async def parse_id(self, text):
        try:
            text = int(text)
        except ValueError:
            pass
        return await self.get_peer_id(text)
