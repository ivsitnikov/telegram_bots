import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    punktuaion_marks = ",.:;!?"
    end = start + size
    while text[start:end].startswith(" "):
        start += 1
    if text[start:end].endswith(tuple(punktuaion_marks)):
        if text[start : end + 1].endswith(tuple(punktuaion_marks)):
            chunk = text[start:end].rsplit(" ", 1)
            logger.info(f"{chunk}: {type(chunk)}")
            return chunk, len(chunk)
        else:
            chunk = text[start:end]
            logger.info(f"{chunk}: {type(chunk)}")
            return chunk, len(chunk)
    else:
        chunk = text[start:end].rsplit(" ", 1)
        logger.info(f"{chunk}: {type(chunk)}")
        return chunk[0], len(chunk[0])


def prepare_book(path: str, page_size: int = 1050) -> dict[int, str]:
    #    prepare_book = {}
    #    with open(path, "r") as book:
    #        _get_part_text(book, 0, 1050)
    #    return prepare_book
    ...


if __name__ == "__main__":
    print(
        *_get_part_text(
            "— Я всё очень тщательно проверил, — сказал компьютер, — и со всей определённостью заявляю, что это и есть ответ. Мне кажется, если уж быть с вами абсолютно честным, то всё дело в том, что вы сами не знали, в чём вопрос.",
            54,
            70,
        ),
        sep="\n",
    )
