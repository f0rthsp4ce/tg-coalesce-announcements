"""Monitor channels, filter out announcements, format them, and forward to a chat."""

import asyncio
from dataclasses import dataclass
import json
import os
import logging
import telethon
import telethon.sessions
import openai as openai_
import filter
import format


@dataclass
class App:
    tg: telethon.TelegramClient
    openai: openai_.AsyncClient
    config: dict


async def process_message(app: App, msg: telethon.types.Message):
    if not msg.message:
        return
    # print(msg.message)

    prompt = {"role": "user", "content": msg.message}
    completion = await app.openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[filter.SYSTEM, prompt],
        tools=filter.TOOLS,
    )
    tool_calls = completion.choices[0].message.tool_calls
    assert tool_calls
    args_str = tool_calls[0].function.arguments
    flag = json.loads(args_str)["flag"]

    # print(flag)
    if not flag:
        return

    completion = await app.openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[format.SYSTEM, prompt],
    )
    content = completion.choices[0].message.content
    assert content
    # print(content)

    await app.tg.send_message(app.config["bot"]["forward-to"], content)
    await app.tg.send_message(
        app.config["bot"]["forward-to"],
        f"Via https://t.me/c/{msg.peer_id.channel_id}/{msg.id}",
    )


async def amain():
    config = json.load(open("settings.json"))

    async with telethon.TelegramClient(
        telethon.sessions.StringSession(os.environ["TELEGRAM_SESSION_TELETHON"]),
        int(os.environ["TELEGRAM_API_ID"]),
        os.environ["TELEGRAM_API_HASH"],
    ) as tg, openai_.AsyncClient() as openai:
        app = App(tg, openai, config)
        for chat in config["bot"]["monitor-chats"]:
            async for msg in tg.iter_messages(chat):
                await process_message(app, msg)
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
