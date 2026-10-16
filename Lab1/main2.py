import os
import re
import argparse

def read():
    with open("data.txt", "r", encoding="utf-8") as file:
            text=file.read()
    return text

match_name=re.compile(r'^[А-ЯA-Z][а-яa-z]+')
def is_valid_name(value:str):
    return bool(match_name.fullmatch(value))

match_sex=re.compile(r'М|м|Мужской|мужской|Ж|ж|Женский|женский|')
def is_valid_sex(value:str):
    return bool(match_sex.fullmatch(value))

match_date=re.compile(r'(\d{1,2})[./-](\d{1,2})[./-](\d{4})')
def is_valid_date(value: str):
    """
    Проверяет корректность даты рождения.

    :param value: значение поля
    :return: True, если валидно
    """
    match = match_date.fullmatch(value)
    if not match:
        return False
    day, month, year = map(int, match.groups())
    if not (1 <= day <= 31 and 1 <= month <= 12):
        return False
    if not (1900 <= year <= 2026):
        return False
    return True

match_num=re.compile(r'(\+7|8)\s*\(?\d{3}\)?[\s-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}')
def is_valid_num(value:str):
    digits = re.sub(r'\D', '', value)
    if len(digits) != 11:
        return False
    if not (digits.startswith('7') or digits.startswith('8')):
        return False
    return bool(match_num.fullmatch(value))
    
match_mail=re.compile(r'[\w.%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)')
def is_valid_mail(value:str):
    return bool(match_mail.fullmatch(value))

match_city=re.compile(r'(г\.\s*)?[А-ЯЁ][а-яё\-]+(\s[А-ЯЁ][а-яё\-]+)*')
def is_valid_city(value:str):
    return bool(match_city.fullmatch(value))

def parse_block(block: str):
    """
    Превращает текст 1 блока в словарь {метка: значение}.

    :param block: текст одной анкеты
    :return: словарь полей
    """
    fields: dict[str, str] = {}
    for line in block.split('\n'):
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        fields[key.strip()] = value.strip()
    return fields

def is_valid_record(fields: dict[str, str]):
    """
    Проверяет, все ли поля анкеты валидны.

    :param fields: словарь полей анкеты
    :return: True, если все поля валидны
    """
    if not is_valid_name(fields.get('Фамилия', '')):
        return False
    if not is_valid_name(fields.get('Имя', '')):
        return False
    if not is_valid_sex(fields.get('Пол', '')):
        return False
    if not is_valid_date(fields.get('Дата рождения', '')):
        return False

    contact = fields.get('Номер телефона или email', '')
    if not (is_valid_num(contact) or is_valid_mail(contact)):
        return False

    if not is_valid_city(fields.get('Город', '')):
        return False

    return True

def print_record(index: int, fields: dict[str, str]):
    """
    Красиво печатает одну валидную анкету.

    :param index: порядковый номер анкеты
    :param fields: словарь полей анкеты
    """
    print(f"--- Анкета №{index} ---")
    for key in ('Фамилия', 'Имя', 'Пол', 'Дата рождения',
                'Номер телефона или email', 'Город'):
        print(f"  {key}: {fields.get(key, '—')}")
    print()


def main():
    """
    Точка входа в программу.
    """
    with open("data.txt", "r", encoding="utf-8") as file:
        text = file.read()

    blocks = re.split(r'\n\d+\)\n', text)
    blocks = [b.strip() for b in blocks if b.strip()]

    valid_records: list[dict[str, str]] = []

   
    for block in blocks:
        fields = parse_block(block)
        if is_valid_record(fields):
            valid_records.append(fields)

   
    print(f"Найдено корректных анкет: {len(valid_records)} "
          f"из {len(blocks)}\n")

    for i, fields in enumerate(valid_records, start=1):
        print_record(i, fields)

if __name__ == '__main__':
    main()