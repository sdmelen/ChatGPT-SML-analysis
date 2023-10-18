from tagger import Tagger, Comments
from dialog import dialog, dark_dialog
import pandas as pd


def save_to_excel(file_name: str, tags: list[str], coms: list[str]) -> None:
    tags_series = pd.Series(tags, name="Теги")
    coms_series = pd.Series(coms, name="Комментарии")
    
    df = pd.concat([coms_series, tags_series], axis=1)

    with pd.ExcelWriter(file_name) as writer:
        df.to_excel(writer)

def make_tags() -> None:
    comments = Comments("БАЗА энергетики_ТЕСТ.xlsx")
    tagger = Tagger(comments)

    tags = tagger.get_tags_for_comments()
    coms = comments.all_comments()

    save_to_excel("tags.xlsx", tags, coms)

    # for i in range(min(len(coms), len(tags))):
        # print("--Комментарий--", coms[i], "--Теги--", tags[i], sep="\n")


if __name__ == "__main__":
    make_tags()



