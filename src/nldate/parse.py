import calendar
import re
from datetime import date, timedelta

_WEEKDAYS: dict[str, int] = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}

_MONTHS: dict[str, int] = {
    "january": 1,
    "jan": 1,
    "february": 2,
    "feb": 2,
    "march": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "may": 5,
    "june": 6,
    "jun": 6,
    "july": 7,
    "jul": 7,
    "august": 8,
    "aug": 8,
    "september": 9,
    "sep": 9,
    "sept": 9,
    "october": 10,
    "oct": 10,
    "november": 11,
    "nov": 11,
    "december": 12,
    "dec": 12,
}

_WORDS: dict[str, int] = {
    "a": 1,
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}

_UNITS: dict[str, str] = {
    "day": "days",
    "days": "days",
    "week": "weeks",
    "weeks": "weeks",
    "month": "months",
    "months": "months",
    "year": "years",
    "years": "years",
}


def _num(s: str) -> int:
    s = s.strip().lower()
    if s in _WORDS:
        return _WORDS[s]
    return int(s)


def _add_months(d: date, n: int) -> date:
    month = d.month + n
    year = d.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    max_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(d.day, max_day))


def _shift(d: date, n: int, unit: str) -> date:
    if unit == "days":
        return d + timedelta(days=n)
    if unit == "weeks":
        return d + timedelta(weeks=n)
    if unit == "months":
        return _add_months(d, n)
    return _add_months(d, n * 12)


def _parse_absolute(s: str) -> date | None:
    m = re.fullmatch(r"(\w+)\s+(\d+)(?:st|nd|rd|th)?,?\s*(\d{4})", s)
    if m:
        mon = _MONTHS.get(m.group(1))
        if mon is not None:
            try:
                return date(int(m.group(3)), mon, int(m.group(2)))
            except ValueError:
                pass
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    return None


def parse(s: str, today: date | None = None) -> date:
    """Parse a natural-language date string and return a datetime.date.

    The optional ``today`` parameter sets the reference date for relative
    expressions such as "tomorrow" or "next Tuesday". Defaults to the
    current date when omitted.
    """
    if today is None:
        today = date.today()

    norm = s.strip().lower()

    # simple keywords
    if norm in ("today", "now"):
        return today
    if norm == "tomorrow":
        return today + timedelta(days=1)
    if norm == "yesterday":
        return today - timedelta(days=1)
    if norm == "the day after tomorrow":
        return today + timedelta(days=2)
    if norm == "the day before yesterday":
        return today - timedelta(days=2)

    # "next <token>"
    m = re.fullmatch(r"next (\w+)", norm)
    if m:
        token = m.group(1)
        wd = _WEEKDAYS.get(token)
        if wd is not None:
            ahead = (wd - today.weekday()) % 7 or 7
            return today + timedelta(days=ahead)
        if token == "week":
            return today + timedelta(weeks=1)
        if token == "month":
            return _add_months(today, 1)
        if token == "year":
            return _add_months(today, 12)

    # "last <token>"
    m = re.fullmatch(r"last (\w+)", norm)
    if m:
        token = m.group(1)
        wd = _WEEKDAYS.get(token)
        if wd is not None:
            behind = (today.weekday() - wd) % 7 or 7
            return today - timedelta(days=behind)
        if token == "week":
            return today - timedelta(weeks=1)
        if token == "month":
            return _add_months(today, -1)
        if token == "year":
            return _add_months(today, -12)

    # "this <weekday>"  — nearest occurrence, including today (0–6 days ahead)
    m = re.fullmatch(r"this (\w+)", norm)
    if m:
        wd = _WEEKDAYS.get(m.group(1))
        if wd is not None:
            ahead = (wd - today.weekday()) % 7
            return today + timedelta(days=ahead)

    # "in <n> <unit1> and <n> <unit2>"  (compound — before simple "in")
    m = re.fullmatch(r"in (\w+) (\w+) and (\w+) (\w+)", norm)
    if m:
        unit1 = _UNITS.get(m.group(2))
        unit2 = _UNITS.get(m.group(4))
        if unit1 is not None and unit2 is not None:
            try:
                d = _shift(today, _num(m.group(1)), unit1)
                return _shift(d, _num(m.group(3)), unit2)
            except ValueError:
                pass

    # "in <n> <unit>"
    m = re.fullmatch(r"in (\w+) (\w+)", norm)
    if m:
        unit = _UNITS.get(m.group(2))
        if unit is not None:
            try:
                return _shift(today, _num(m.group(1)), unit)
            except ValueError:
                pass

    # "<n> <unit> ago"
    m = re.fullmatch(r"(\w+) (\w+) ago", norm)
    if m:
        unit = _UNITS.get(m.group(2))
        if unit is not None:
            try:
                return _shift(today, -_num(m.group(1)), unit)
            except ValueError:
                pass

    # compound: "<n1> <unit1> and <n2> <unit2> before/after <ref>"
    m = re.fullmatch(r"(\w+) (\w+) and (\w+) (\w+) (before|after) (.+)", norm)
    if m:
        unit1 = _UNITS.get(m.group(2))
        unit2 = _UNITS.get(m.group(4))
        if unit1 is not None and unit2 is not None:
            try:
                n1, n2 = _num(m.group(1)), _num(m.group(3))
                sign = 1 if m.group(5) == "after" else -1
                ref = parse(m.group(6), today=today)
                return _shift(_shift(ref, sign * n1, unit1), sign * n2, unit2)
            except ValueError:
                pass

    # "<n> <unit> from/after <ref>"
    m = re.fullmatch(r"(\w+) (\w+) (?:from|after) (.+)", norm)
    if m:
        unit = _UNITS.get(m.group(2))
        if unit is not None:
            try:
                ref = parse(m.group(3), today=today)
                return _shift(ref, _num(m.group(1)), unit)
            except ValueError:
                pass

    # "<n> <unit> before <ref>"
    m = re.fullmatch(r"(\w+) (\w+) before (.+)", norm)
    if m:
        unit = _UNITS.get(m.group(2))
        if unit is not None:
            try:
                ref = parse(m.group(3), today=today)
                return _shift(ref, -_num(m.group(1)), unit)
            except ValueError:
                pass

    result = _parse_absolute(norm)
    if result is not None:
        return result

    raise ValueError(f"Cannot parse date: {s!r}")
