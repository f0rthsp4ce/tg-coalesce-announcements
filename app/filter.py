import openai.types.chat

SYSTEM: openai.types.chat.ChatCompletionSystemMessageParam = {
    "role": "system",
    "content": "You filter chat messages looking for announcements. An event announcement typically contains time and date, and event name or topic.",
}

TOOLS: list[openai.types.chat.ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "is_announcement",
            "description": "Judge if given message is an announcement",
            "parameters": {
                "type": "object",
                "properties": {
                    "flag": {
                        "type": "boolean",
                    },
                },
                "required": ["flag"],
            },
        },
    },
]
