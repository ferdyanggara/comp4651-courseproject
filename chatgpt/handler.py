import json
import requests

from dotenv import dotenv_values

config = dotenv_values()
api_url = "https://chatgpt-api.shn.hk/v1"
openai_api_key = config["OPENAI_API_KEY"]


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    response = None
    content = None
    dict = None

    try:
        req = json.loads(req)
        user_id = req["user_id"]
        chatgpt_bot_id = req["chatgpt_bot_id"]
        messages = req["messages"]

        conversationLog = []
        count = 0
        for msg in messages[::-1]:
            # Only get the last 20 messages
            if count == 20:
                break
            if str(msg["author_id"]) == str(user_id):
                conversationLog.append(
                    {"role": "user", "content": msg["content"].removeprefix("!chat")}
                )
                count += 1
            elif not msg["content"].startswith("!chat"):
                continue
            elif str(msg["author_id"]) == str(chatgpt_bot_id):
                conversationLog.append({"role": "assistant", "content": msg["content"]})
                count += 1

        conversationLog.reverse()

        data = json.dumps(
            {
                "model": "gpt-3.5-turbo",
                "messages": conversationLog,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}",
        }

        response = requests.post(api_url, data=data, headers=headers)
        content = response.content.decode("utf-8")
        dict = json.loads(content)

        return dict["choices"][0]["message"]["content"]
    except json.JSONDecodeError:
        try:
            content = content.removeprefix("OpenAI API responded:")
            dict = json.loads(content)
        except Exception:
            return "Something went wrong. Please try again later."

        if dict["error"] and dict["error"]["message"]:
            return dict["error"]["message"]
        else:
            return "Something went wrong. Please try again later."
