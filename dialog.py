from chatGPT import ChatGPT

def dialog() -> None:
    chat = ChatGPT()

    while True:
        ask_text = input("#User: ")
        response = chat.ask(ask_text)
        print("#ChatGPT:", response)

def dark_dialog() -> None:
    chat = ChatGPT()

    with open("prompt_dark.txt", "r", encoding="utf8") as f:
        prompt_text = "\n".join(f.readlines())
        chat.add_prompt(prompt_text)

    while True:
        ask_text = input("#User: ")
        response = chat.ask(ask_text)
        print("#ChatGPT:", response)