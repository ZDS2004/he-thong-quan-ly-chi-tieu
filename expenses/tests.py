from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from expenses.forms import TransactionForm
from expenses.models import Note, Transaction
from expenses.services import month_summary


class ExpenseModelTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("an", password="matkhau123")
        self.other = User.objects.create_user("binh", password="matkhau123")

    def test_signup_seeds_default_categories(self) -> None:
        names = set(self.user.categories.values_list("name", flat=True))
        self.assertIn("Ăn uống", names)
        self.assertIn("Lương", names)

    def test_amount_must_be_positive(self) -> None:
        cat = self.user.categories.get(name="Ăn uống")
        tx = Transaction(
            user=self.user,
            category=cat,
            amount=Decimal("0"),
            occurred_on=date(2026, 11, 1),
        )
        with self.assertRaises(ValidationError):
            tx.full_clean()

    def test_cannot_use_someone_elses_category(self) -> None:
        cat = self.other.categories.get(name="Ăn uống")
        tx = Transaction(
            user=self.user,
            category=cat,
            amount=Decimal("10000"),
            occurred_on=date(2026, 11, 1),
        )
        with self.assertRaises(ValidationError):
            tx.full_clean()


class MonthSummaryTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("an", password="matkhau123")
        self.eat = self.user.categories.get(name="Ăn uống")
        self.salary = self.user.categories.get(name="Lương")

    def test_aggregates_current_month_only(self) -> None:
        Transaction.objects.create(
            user=self.user, category=self.salary, amount=10_000_000, occurred_on=date(2026, 11, 1)
        )
        Transaction.objects.create(
            user=self.user, category=self.eat, amount=50_000, occurred_on=date(2026, 11, 2)
        )
        Transaction.objects.create(
            user=self.user, category=self.eat, amount=99_000, occurred_on=date(2026, 10, 30)
        )
        summary = month_summary(self.user, 2026, 11)
        self.assertEqual(summary.income, Decimal("10000000"))
        self.assertEqual(summary.expense, Decimal("50000"))
        self.assertEqual(summary.balance, Decimal("9950000"))
        self.assertEqual(summary.by_category[0]["name"], "Ăn uống")

class MoneyInputFormTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("money-user", password="matkhau123")

    def test_transaction_form_accepts_grouped_vietnamese_amount(self) -> None:
        category = self.user.categories.get(name="Lương")
        form = TransactionForm(
            data={
                "category": category.pk,
                "amount": "5.000.000 đ",
                "occurred_on": "2026-11-08",
                "note": "Lương tháng",
            },
            user=self.user,
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["amount"], Decimal("5000000"))

    def test_existing_transaction_amount_displays_with_grouping(self) -> None:
        category = self.user.categories.get(name="Lương")
        transaction = Transaction(
            user=self.user,
            category=category,
            occurred_on=date(2026, 11, 8),
            amount=Decimal("5000000"),
        )
        form = TransactionForm(instance=transaction, user=self.user)

        self.assertEqual(form["amount"].value(), "5.000.000")


class NoteFlowTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("ghi-chu-user", password="matkhau123")
        self.other = User.objects.create_user("ghi-chu-other", password="matkhau123")

    def test_user_can_create_and_view_a_note(self) -> None:
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("expenses:note_create"),
            {"note_date": "2026-11-08", "content": "Nhắc đóng học phí"},
        )

        self.assertEqual(response.status_code, 302)
        note = Note.objects.get(user=self.user)
        page = self.client.get(reverse("expenses:note_list"))
        self.assertContains(page, "Nhắc đóng học phí")
        self.assertEqual(note.content, "Nhắc đóng học phí")
        self.assertEqual(note.note_date, date(2026, 11, 8))

    def test_user_cannot_open_another_users_note_for_editing(self) -> None:
        note = Note.objects.create(user=self.user, content="Ghi chú riêng")
        self.client.force_login(self.other)

        response = self.client.get(reverse("expenses:note_update", args=[note.pk]))

        self.assertEqual(response.status_code, 404)


class AuthFlowTests(TestCase):
    def test_register_and_see_dashboard(self) -> None:
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "chi",
                "password1": "sieu-bi-mat-99",
                "password2": "sieu-bi-mat-99",
            },
        )
        self.assertEqual(response.status_code, 302)
        home = self.client.get(reverse("dashboard:home"))
        self.assertEqual(home.status_code, 200)
        self.assertContains(home, "Túi")
