from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Category(models.Model):
    class Kind(models.TextChoices):
        INCOME = "income", "Thu"
        EXPENSE = "expense", "Chi"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    name = models.CharField("Tên danh mục", max_length=80)
    kind = models.CharField("Loại", max_length=10, choices=Kind.choices)
    color = models.CharField("Màu", max_length=7, default="#3D7A5A")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["kind", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name", "kind"],
                name="uniq_category_per_user_kind",
            )
        ]
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"

    def __str__(self) -> str:
        return f"{self.get_kind_display()} · {self.name}"


class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Danh mục",
    )
    amount = models.DecimalField(
        "Số tiền (VNĐ)",
        max_digits=14,
        decimal_places=0,
        validators=[MinValueValidator(Decimal("1"))],
    )
    occurred_on = models.DateField("Ngày", default=timezone.localdate)
    note = models.CharField("Ghi chú", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_on", "-created_at"]
        verbose_name = "Giao dịch"
        verbose_name_plural = "Giao dịch"

    def clean(self) -> None:
        if self.category_id and self.user_id and self.category.user_id != self.user_id:
            raise ValidationError("Danh mục không thuộc về tài khoản này.")

    def __str__(self) -> str:
        sign = "+" if self.category.kind == Category.Kind.INCOME else "-"
        return f"{sign}{self.amount} · {self.category.name}"


class Note(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    note_date = models.DateField("Ngày ghi chú", default=timezone.localdate)
    content = models.TextField("Nội dung ghi chú")
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
    updated_at = models.DateTimeField("Cập nhật lần cuối", auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Ghi chú"
        verbose_name_plural = "Ghi chú"

    def __str__(self) -> str:
        return self.content[:60]


class MonthlyBudget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="budgets",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="budgets",
        verbose_name="Danh mục chi",
    )
    year = models.PositiveIntegerField("Năm")
    month = models.PositiveSmallIntegerField("Tháng")
    limit = models.DecimalField(
        "Hạn mức (VNĐ)",
        max_digits=14,
        decimal_places=0,
        validators=[MinValueValidator(Decimal("1"))],
    )

    class Meta:
        ordering = ["-year", "-month", "category__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "category", "year", "month"],
                name="uniq_budget_per_category_month",
            ),
            models.CheckConstraint(
                condition=models.Q(month__gte=1, month__lte=12),
                name="budget_month_1_12",
            ),
        ]
        verbose_name = "Ngân sách tháng"
        verbose_name_plural = "Ngân sách tháng"

    def clean(self) -> None:
        if self.category_id and self.category.kind != Category.Kind.EXPENSE:
            raise ValidationError("Ngân sách chỉ áp dụng cho danh mục chi.")
        if self.category_id and self.user_id and self.category.user_id != self.user_id:
            raise ValidationError("Danh mục không thuộc về tài khoản này.")

    def __str__(self) -> str:
        return f"{self.category.name} {self.month:02d}/{self.year}: {self.limit}"
