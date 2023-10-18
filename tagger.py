import pandas as pd
from chatGPT import ChatGPT

from math import ceil

class Comments:
    def __init__(self, file_name: str) -> None:
        self.df = pd.read_excel(file_name)

    def get(self, page: int, per_page: int) -> list[str]:
        try:
            return list(self.df["Текст"][page * per_page:(page + 1) * per_page])
        except:
            return []
        
    def page_amount(self, per_page: int) -> int:
        return len(self.df) // per_page + (0 if len(self.df) % per_page == 0 else 1)
    
    def generator(self, per_page: int = 10) -> list[str]:
        for i in range(self.page_amount(per_page)):
            yield self.get(i, per_page)
            
    def all_comments(self) -> list[str]:
        return list(self.df["Текст"])


class Tagger:
    def __init__(self, comments: Comments) -> None:
        self.comments = comments
        self.chat = ChatGPT()

    def get_prompt(self, comments_list: list[str]) -> str:
        prompt_text = (f"Тебе представлено {len(comments_list)} комментариев. "
        "Каждый комментарий начинается с символа № и соответствующего номера. " 
        "Ты исследуешь, как комментатор относится к энергетическим напиткам. "
        "Под каждый комментарий составь сообщения следующего вида (приведены четыре примера оформления):\n"
        "№1 Вкус: хороший, насыщенный; Цена: низкая; Качество: отличное.\n"
        "№2 Вкус: средний; Аромат: приторный; Вид: красивый.\n"
        "№3 Пропуск.\n"
        "№4 Дизайн: удобная упаковка; Наличие: нигде нет.\n"
        "Характеристика должна быть быть общей, выражать мнение клиента, содержать одно или два слова. "
        "Если по какой-то характеристике нет информации в комментарии, то характеристика не указывается. "
        "Если в комментарии нет полезных характеристик, то пишется слово пропуск. "
        "Есть только следующие характеристики: Вкус, Цена, Качество, Аромат, Вид, Дизайн, Наличие. "
        "Другие характеристики не рассматривать. Слова \"Характеристики\" быть не должно")

        return prompt_text

    def parse_response(self, response_text: str) -> list[str]:
        tags_list = []
        for t in response_text.split("№"):
            try:
                t = t[2:].replace("\n", "")
                if t.lower().strip() == "пропуск." and t.lower().strip() == "пропуск":
                    tags_list.append("")
                else:
                    tags_list.append(t)
            except:
                tags_list.append("")
        
        return tags_list[1:]

    def get_tags(self, comments_list: list[str]) -> list[str]:
        self.chat.clear()
        self.chat.add_prompt(self.get_prompt(comments_list))
        self.chat.add_user_message("\n".join([f"№{i + 1} {comments_list[i]}" for i in range(len(comments_list))]))
        return self.parse_response(self.chat.send())

    def get_tags_for_comments(self) -> list[str]:
        tags_list = []
        per_page = 10
        for comments_list in self.comments.generator(per_page=per_page):
            try:
                tags = self.get_tags(comments_list)
            except:
                try:
                    tags = self.get_tags(comments_list[0:len(comments_list) // 2]) + self.get_tags(comments_list[len(comments_list) // 2:])
                except:
                    tags = ["" for i in range(per_page)]
                

            if len(tags) != len(comments_list):
                while len(tags) > len(comments_list):
                    tags.pop()
                while len(tags) < len(comments_list):
                    tags.append("")

            tags_list.extend(tags)

            print("Прочитаны 10 записей")

        return tags_list

    

    # def get_tags_single(self, comment: str) -> None:
    #     self.chat.clear()
    #     self.chat.add_prompt(f"")
    #     self.chat.add_user_message("\n".join([f"№{i + 1} {comments_list[i]}" for i in range(len(comments_list))]))
    #     print(self.chat.send())

    # def get_tags_for_comments_single(self) -> None:
    #     for comments_list in self.comments.generator(per_page=1):
    #         self.get_tags_single(comments_list[0])



    