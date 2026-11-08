from decimal import Decimal

from django import template

from expenses.services import format_vnd

register = template.Library()


@register.filter
def vnd(value) -> str:
    if value is None or value == "":
        return "0 ₫"
    return format_vnd(Decimal(value))
