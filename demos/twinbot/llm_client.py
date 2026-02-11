from dataclasses import dataclass
import streamlit as st
from openai import OpenAI

@dataclass(frozen=True)
class Turn:
    user: str
    assistant: str

@st.cache_resource(show_spinner=False)
def get_openai_client(base_url: str, api_key: str) -> OpenAI:
    return OpenAI(base_url=base_url, api_key=api_key)

def chat_completion(
    *,
    client: OpenAI,
    model: str,
    system_prompt: str,
    user_message: str,
    history: list[Turn],
) -> str:
    messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
    for h in history:
        messages.append({"role": "user", "content": h.user})
        messages.append({"role": "assistant", "content": h.assistant})
    messages.append({"role": "user", "content": user_message})

    resp = client.chat.completions.create(model=model, messages=messages)
    answer = (resp.choices[0].message.content or "").strip()
    return answer
