from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from expenses.models import Category, Transaction


class Command(BaseCommand):
    help = "Tạo tài khoản demo và vài giao dịch mẫu để quay video."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username="demo", defaults={"email": "demo@example.com"}
        )
        user.set_password("demo12345")
        user.save()

        today = timezone.localdate()
        eat = Category.objects.get(user=user, name="Ăn uống")
        travel = Category.objects.get(user=user, name="Đi lại")
        study = Category.objects.get(user=user, name="Học tập")
        salary = Category.objects.get(user=user, name="Lương")

        Transaction.objects.filter(user=user).delete()

        samples = [
            (salary, Decimal("12000000"), date(today.year, today.month, 1), "Lương tháng"),
            (eat, Decimal("85000"), date(today.year, today.month, 2), "Cơm trưa"),
            (eat, Decimal("120000"), date(today.year, today.month, 5), "Cafe + bánh"),
            (travel, Decimal("50000"), date(today.year, today.month, 3), "Grab"),
            (study, Decimal("350000"), date(today.year, today.month, 7), "Sách Django"),
            (eat, Decimal("210000"), date(today.year, today.month, 10), "Đi ăn tối"),
        ]
        Transaction.objects.bulk_create(
            [
                Transaction(
                    user=user,
                    category=cat,
                    amount=amount,
                    occurred_on=day,
                    note=note,
                )
                for cat, amount, day, note in samples
            ]
        )
        self.stdout.write(self.style.SUCCESS("OK. Login: demo / demo12345"))
