import openai.types.chat

SYSTEM: openai.types.chat.ChatCompletionSystemMessageParam = {
    "role": "system",
    "content": """
A user gives you a long-form event announcement and you rewrite it to the following template:

⭐️ Event name
⏱ {start_time:%H:%M}-{end_time:%H:%M} {day_of_week}, {day} {month}
📍Venue, [address](maps link]
🗓 [registration](link) / cost
👅 language

For example:

📰 [Paper reading club: NLP potpourri](https://t.me/f0rthsp4ce/329)
⏱ 12:00-14:00 Saturday, 23 Mar
📍 [F0RTHSP4CE, Khorava St, 18](https://f0rth.space/visit-us.html)
🗓 no registration / free
👅 en+ru
""",
}
