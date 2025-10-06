import random

from lexicon import LEXICON_RU


# Функция для определения выбора бота
def get_bot_choice():
    return random.choice(["rock", "papper", "scissors"])


def _normalaize_user_answer(user_answer: str):
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            break
        return key


def get_winner(user_answer: str, bot_choice: str) -> str:
    user_choice = _normalaize_user_answer(user_answer)
    rules = {"rock": "scissors", "papper": "rock", "scissors": "papper"}
    if user_choice == bot_choice:
        return "nobody_won"
    elif rules[user_choice] == bot_choice:
        return "user_won"
    return "bot_won"


if __name__ == "__main__":
    bot_choice = get_bot_choice()
    user_answer = "Камень \U0001f91c"
    user_choice = "rock"
    print(user_choice)
    print(get_winner(user_choice, bot_choice))
