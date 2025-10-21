from pathlib import Path
import re
import json
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    pattern_marks = r"[,.:;!?]"
    right_border = start + size
    page = text[start:right_border]
    logger.info(f"Страница:\n{page}\n Длина страницы {len(page)}")
    marks_from_page = list(re.finditer(pattern_marks, page))
    logger.info(f"Знаки препинания на странице и их позиции  {marks_from_page}")
    # Проверка кейсов
    if marks_from_page:
        # Каждая страница должна закончиться знаком препинания
        end_page = marks_from_page[-1].end()
        logger.info(f"Позиция конца страницы установлена на значении {end_page}")
        # Знак препинания находится на границе страницы
        if end_page == len(page):
            logger.info("Страница закончилась знаком препинания")
            try:
                logger.info(
                    f"Проверяем символ следующий за концом страницы '{text[right_border]}'"
                )
                assert text[right_border] in list(pattern_marks)
                logger.info(f"Cимвол следующий за концом страницы - знак препинания")
                end_page = marks_from_page[-2].end()
                logger.info(f"Позиция конца страницы изменена {end_page}")
            except AssertionError:
                logger.info(
                    f"Cимвол следующий за концом куска текста не знак препинания"
                )
            except IndexError:
                logger.info("Достигнут конец документа")
            try:
                logger.info(f"Проверяем символ перед страницей")
                assert marks_from_page[-2].end() == len(page) - 1
                logger.info(f"Предыдущий символ - знак препинания")
                end_page = marks_from_page[-3].end()
                logger.info(f"Позиция конца страницы изменена {end_page}")
            except AssertionError:
                logger.info(f"Предпоследний символ не знак припенания")

        page = page[0:end_page].lstrip()
    return page, len(page)


def prepare_book(path: str, page_size: int = 1050) -> dict[int, str]:
    book_dict: dict[int, str] = {}

    with open(path, "r", encoding="utf-8") as book:
        text = book.read()
        text_size = len(text)
        start, page_number = 0, 1
        offset = 0
        while text_size > start:
            page_text, offset = _get_part_text(text, start, page_size)
            book_dict.setdefault(page_number, page_text.lstrip())
            page_number += 1
            start += offset
    return book_dict


if __name__ == "__main__":
    text = """Пошлость собственной мечты была так заметна, что Таня понимала: даже мечтать и горевать ей 
    приходится закачанными в голову штампами, и по­другому не может быть, потому что через все женски
    е головы на планете давно проложена ржавая узкоколейка, и эти мысли — вовсе не ее собственные надежды
    , а просто грохочущий у нее в мозгу коммерческий товарняк.
Словно бы на самом деле думала и мечтала не она, а в пустом осеннем сквере горела на стене
дома огромная панель, показывая равнодушным жирным воронам рекламу бюджетной косметики."""

    # print(*_get_part_text(text, 0, 100), sep="\n")
    logger.debug({Path.cwd()})
    path = Path.cwd() / "book" / "Bredberi_Marsianskie-hroniki.txt"
    # path = Path.cwd() / "book" / "test.txt"
    logger.debug({path})
    logger.debug(
        json.dumps(prepare_book(path), indent=2, sort_keys=True, ensure_ascii=False)
    )
