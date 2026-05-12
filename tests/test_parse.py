from datetime import date

import pytest

from nldate import parse

# Fixed reference date: 2025-06-15 (Sunday)
REF = date(2025, 6, 15)


def test_today() -> None:
    assert parse("today", today=REF) == REF


def test_tomorrow() -> None:
    assert parse("tomorrow", today=REF) == date(2025, 6, 16)


def test_yesterday() -> None:
    assert parse("yesterday", today=REF) == date(2025, 6, 14)


def test_next_tuesday_from_sunday() -> None:
    # Sunday -> next Tuesday is 2 days ahead
    assert parse("next Tuesday", today=REF) == date(2025, 6, 17)


def test_next_weekday_same_day_wraps() -> None:
    # "next Sunday" from Sunday should be 7 days ahead, not today
    assert parse("next Sunday", today=REF) == date(2025, 6, 22)


def test_last_monday_from_sunday() -> None:
    # Sunday June 15 — last Monday is June 9 (6 days ago)
    assert parse("last Monday", today=REF) == date(2025, 6, 9)


def test_in_n_days() -> None:
    assert parse("in 5 days", today=REF) == date(2025, 6, 20)


def test_in_n_weeks() -> None:
    assert parse("in 2 weeks", today=REF) == date(2025, 6, 29)


def test_in_n_months() -> None:
    assert parse("in 3 months", today=REF) == date(2025, 9, 15)


def test_in_n_years() -> None:
    assert parse("in 1 year", today=REF) == date(2026, 6, 15)


def test_n_days_ago() -> None:
    assert parse("3 days ago", today=REF) == date(2025, 6, 12)


def test_days_before_absolute_date() -> None:
    # "5 days before December 1st, 2025" — no today needed (absolute ref)
    assert parse("5 days before December 1st, 2025") == date(2025, 11, 26)


def test_days_after_absolute_date() -> None:
    assert parse("3 days after January 10, 2025") == date(2025, 1, 13)


def test_word_number_weeks_from_tomorrow() -> None:
    # "two weeks from tomorrow" — tomorrow is June 16, +14 days = June 30
    assert parse("two weeks from tomorrow", today=REF) == date(2025, 6, 30)


def test_compound_year_and_month_after_today() -> None:
    # 1 year + 2 months after June 15, 2025 = August 15, 2026
    assert parse("1 year and 2 months after today", today=REF) == date(2026, 8, 15)


def test_compound_year_and_month_after_relative() -> None:
    # 1 year + 2 months after yesterday (June 14, 2025) = August 14, 2026
    assert parse("1 year and 2 months after yesterday", today=REF) == date(2026, 8, 14)


def test_absolute_date_with_ordinal() -> None:
    assert parse("December 25th, 2025") == date(2025, 12, 25)


def test_absolute_date_without_ordinal() -> None:
    assert parse("January 1, 2026") == date(2026, 1, 1)


def test_iso_date() -> None:
    assert parse("2026-01-15") == date(2026, 1, 15)


def test_month_end_clamping() -> None:
    # March 31 + 1 month = April 30 (not April 31, which doesn't exist)
    assert parse("in 1 month", today=date(2025, 3, 31)) == date(2025, 4, 30)


def test_invalid_input_raises() -> None:
    with pytest.raises(ValueError):
        parse("not a date at all")
