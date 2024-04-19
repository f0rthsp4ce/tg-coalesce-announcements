"""Monitor channels, filter out announcements, format them, and forward to a chat."""

import asyncio
import json
import os
import logging
import telethon
import telethon.sessions
import openai as openai_
import filter
import format


async def amain():
    config = json.load(open("settings.json"))

    async with telethon.TelegramClient(
        telethon.sessions.StringSession(os.environ["TELEGRAM_SESSION_TELETHON"]),
        int(os.environ["TELEGRAM_API_ID"]),
        os.environ["TELEGRAM_API_HASH"],
    ) as tg, openai_.AsyncClient() as openai:
        for chat in config["bot"]["monitor-chats"]:
            async for msg in tg.iter_messages(chat):
                if not msg.message:
                    continue
                # print(msg.message)

                prompt = {"role": "user", "content": msg.message}
                completion = await openai.chat.completions.create(
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
                    continue

                completion = await openai.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[format.SYSTEM, prompt],
                )
                print(completion.choices[0].message.content)

                break
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
