from __future__ import annotations

from calendar import monthrange
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import AbstractBaseUser
from django.db.models import QuerySet, Sum
from django.utils import timezone

from .models import Category, Transaction

DEFAULT_CATEGORIES: list[tuple[str, str, str]] = [
    ("Ăn uống", Category.Kind.EXPENSE, "#C45C26"),
    ("Đi lại", Category.Kind.EXPENSE, "#2F6F9F"),
    ("Học tập", Category.Kind.EXPENSE, "#3D7A5A"),
    ("Nhà cửa", Category.Kind.EXPENSE, "#8B5E3C"),
    ("Giải trí", Category.Kind.EXPENSE, "#A33B5A"),
    ("Sức khỏe", Category.Kind.EXPENSE, "#4C7C6A"),
    ("Khác", Category.Kind.EXPENSE, "#6B6258"),
    ("Lương", Category.Kind.INCOME, "#1F4D3A"),
    ("Thưởng", Category.Kind.INCOME, "#3D7A5A"),
    ("Khác (thu)", Category.Kind.INCOME, "#5A8F6A"),
]


def seed_default_categories(user: AbstractBaseUser) -> None:
    existing = Category.objects.filter(user=user).exists()
    if existing:
        return
    Category.objects.bulk_create(
        [
            Category(user=user, name=name, kind=kind, color=color)
            for name, kind, color in DEFAULT_CATEGORIES
        ]
    )


def month_bounds(year: int, month: int) -> tuple[date, date]:
    last_day = monthrange(year, month)[1]
    return date(year, month, 1), date(year, month, last_day)


def month_from_query(query) -> tuple[int, int]:
    today = timezone.localdate()

    try:
        year = int(query.get("year", today.year))
    except (TypeError, ValueError):
        year = today.year

    try:
        month = int(query.get("month", today.month))
    except (TypeError, ValueError):
        month = today.month

    if not 1 <= year <= 9999:
        year = today.year
    if not 1 <= month <= 12:
        month = today.month

    return year, month


def owned_transactions(user: AbstractBaseUser) -> QuerySet[Transaction]:
    return Transaction.objects.filter(user=user).select_related("category")


@dataclass(frozen=True)
class MonthSummary:
    year: int
    month: int
    income: Decimal
    expense: Decimal
    balance: Decimal
    by_category: list[dict]
    daily_expense: list[dict]


def _zero() -> Decimal:
    return Decimal("0")


def month_summary(user: AbstractBaseUser, year: int, month: int) -> MonthSummary:
    start, end = month_bounds(year, month)
    qs = owned_transactions(user).filter(occurred_on__range=(start, end))

    income = qs.filter(category__kind=Category.Kind.INCOME).aggregate(total=Sum("amount"))[
        "total"
    ] or _zero()
    expense = qs.filter(category__kind=Category.Kind.EXPENSE).aggregate(total=Sum("amount"))[
        "total"
    ] or _zero()

    by_category_rows = (
        qs.filter(category__kind=Category.Kind.EXPENSE)
        .values("category__name", "category__color")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    by_category = [
        {
            "name": row["category__name"],
            "color": row["category__color"],
            "total": row["total"] or _zero(),
        }
        for row in by_category_rows
    ]

    spent_by_day = {
        row["occurred_on"]: row["total"] or _zero()
        for row in qs.filter(category__kind=Category.Kind.EXPENSE)
        .values("occurred_on")
        .annotate(total=Sum("amount"))
    }
    daily_expense = []
    cursor = start
    while cursor <= end:
        daily_expense.append(
            {"day": cursor.day, "total": spent_by_day.get(cursor, _zero())}
        )
        cursor += timedelta(days=1)

    return MonthSummary(
        year=year,
        month=month,
        income=income,
        expense=expense,
        balance=income - expense,
        by_category=by_category,
        daily_expense=daily_expense,
    )


def format_vnd(value: Decimal | int) -> str:
    return f"{int(value):,}".replace(",", ".") + " ₫"
