"""Monitor channels, filter out announcements, format them, and forward to a chat."""

import asyncio
import json
import os
import logging
import telethon
import telethon.sessions


async def amain():
    config = json.load(open("settings.json"))

    async with telethon.TelegramClient(
        telethon.sessions.StringSession(os.environ["TELEGRAM_SESSION_TELETHON"]),
        int(os.environ["TELEGRAM_API_ID"]),
        os.environ["TELEGRAM_API_HASH"],
    ) as tg:
        for chat in config["bot"]["monitor-chats"]:
            async for msg in tg.iter_messages(chat):
                print(msg)
                break

        # @tg.on(
        #     telethon.events.NewMessage(
        #         chats=config['bot']['monitor-chats'], incoming=True
        #     )
        # )
        # async def h(event):
        #     pass

        # await asyncio.Event().wait()


def main():
    logging.basicConfig(
        format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
        level=logging.WARNING,
    )
    asyncio.run(amain())


if __name__ == "__main__":
    main()
