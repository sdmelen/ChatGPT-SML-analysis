import openai
from enum import Enum

class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class ChatGPT:
    def __init__(self) -> None:
        openai.api_key = "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"
        self.chat_version = "gpt-3.5-turbo"
        self.messages = []

    def add_message(self, role: Role, text: str) -> None:
        self.messages.append({
            "role": role.value,
            "content": text
        })

    def add_prompt(self, prompt_text: str) -> None:
        self.add_message(Role.SYSTEM, prompt_text)

    def add_user_message(self, user_text: str) -> None:
        self.add_message(Role.USER, user_text)

    def add_assistant_message(self, assistant_text: str) -> None:
        self.add_message(Role.ASSISTANT, assistant_text)

    def send(self) -> str:
        completion = openai.ChatCompletion.create(model=self.chat_version, messages=self.messages)
        response_text = completion.choices[0].message.content
        return response_text

    def ask(self, ask_text: str, save_ask: bool=True, save_response: bool=True) -> str:
        self.add_user_message(ask_text)

        response_text = self.send()

        if not save_ask:
            self.messages.pop()

        if save_response:
            self.add_assistant_message(response_text)

        return response_text
    
    def clear(self, clear_system: bool=True, clear_user: bool=True, clear_assistant: bool=True) -> None:
        clears = [clear_system, clear_user, clear_assistant]
        roles = [Role.SYSTEM, Role.USER, Role.ASSISTANT]
        self.messages = list(filter(lambda message: (
            any(message["role"] == r and c for c, r in zip(clears, roles))
        ), self.messages))

