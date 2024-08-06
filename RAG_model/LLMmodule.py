import requests


def get_llm_response(sys_content, user_content):
    url = "https://api.siliconflow.cn/v1/chat/completions"

    payload = {
        "model": "Qwen/Qwen2-7B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": sys_content
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": ""
        # Replace your_token with your actual token
    }

    response = requests.post(url, json=payload, headers=headers)

    response_json = response.json()
    llm_reply = response_json.get("choices")[0].get("message").get("content")

    return llm_reply
