import validators
from dateutil.parser import parse


def is_date(text: str) -> bool:
    try:
        parse(text, yearfirst=True)
        return True
    except ValueError:
        return False


def is_email(text: str) -> bool:
    return validators.email(text)
