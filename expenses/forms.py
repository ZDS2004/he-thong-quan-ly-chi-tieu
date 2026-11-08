from decimal import Decimal

from django import forms
from django.utils import timezone

from .models import Category, Note, Transaction


class VietnameseMoneyField(forms.DecimalField):
    def to_python(self, value):
        if isinstance(value, str):
            value = value.strip().lower()
            value = value.replace("vnđ", "").replace("vnd", "")
            value = value.replace("đ", "").replace("₫", "")
            value = value.replace(".", "").replace(" ", "")
        return super().to_python(value)

    def prepare_value(self, value):
        value = super().prepare_value(value)
        if value in (None, ""):
            return value
        try:
            amount = Decimal(str(value))
        except (TypeError, ValueError):
            return value
        if amount == amount.to_integral_value():
            return f"{int(amount):,}".replace(",", ".")
        return value


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "kind", "color")
        widgets = {
            "color": forms.TextInput(attrs={"type": "color"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned = super().clean()
        name, kind = cleaned.get("name"), cleaned.get("kind")
        if self.user and name and kind:
            qs = Category.objects.filter(user=self.user, name=name, kind=kind)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Danh mục này đã tồn tại.")
        if self.instance.pk and kind and kind != self.instance.kind:
            has_transactions = self.instance.transactions.exists()
            has_budgets = self.instance.budgets.exists()
            if has_transactions or has_budgets:
                raise forms.ValidationError(
                    "Không thể đổi loại danh mục đã có giao dịch hoặc hạn mức đã lưu."
                )
        return cleaned

    def save(self, commit: bool = True) -> Category:
        obj = super().save(commit=False)
        if self.user is not None:
            obj.user = self.user
        if commit:
            obj.save()
        return obj


class TransactionForm(forms.ModelForm):
    amount = VietnameseMoneyField(
        label="Số tiền (VNĐ)",
        max_digits=14,
        decimal_places=0,
        min_value=Decimal("1"),
        help_text="Nhập 5000000 hoặc 5.000.000 đ. Dấu chấm chỉ dùng để phân tách hàng nghìn.",
        error_messages={"invalid": "Nhập số tiền hợp lệ, ví dụ: 5.000.000."},
        widget=forms.TextInput(
            attrs={
                "inputmode": "numeric",
                "autocomplete": "off",
                "placeholder": "Ví dụ: 5.000.000",
                "data-vnd-input": "true",
            }
        ),
    )

    class Meta:
        model = Transaction
        fields = ("category", "amount", "occurred_on", "note")
        widgets = {
            "occurred_on": forms.DateInput(attrs={"type": "date"}),
            "note": forms.TextInput(attrs={"placeholder": "Ghi chú ngắn (tuỳ chọn)"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user is not None:
            self.fields["category"].queryset = Category.objects.filter(user=user)
        if not self.instance.pk:
            self.fields["occurred_on"].initial = timezone.localdate()

    def save(self, commit: bool = True) -> Transaction:
        obj = super().save(commit=False)
        obj.user = self.user
        if commit:
            obj.full_clean()
            obj.save()
        return obj


class NoteForm(forms.ModelForm):
    content = forms.CharField(
        label="Nội dung ghi chú",
        required=True,
        widget=forms.Textarea(
            attrs={"rows": 4, "placeholder": "Nhập ghi chú của bạn..."}
        ),
    )

    class Meta:
        model = Note
        fields = ("note_date", "content")
        widgets = {
            "note_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if not self.instance.pk:
            self.fields["note_date"].initial = timezone.localdate()

    def save(self, commit: bool = True) -> Note:
        obj = super().save(commit=False)
        obj.user = self.user
        if commit:
            obj.full_clean()
            obj.save()
        return obj
