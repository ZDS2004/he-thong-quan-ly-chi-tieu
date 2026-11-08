from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CategoryForm, NoteForm, TransactionForm
from .mixins import OwnedFormMixin, OwnedQuerysetMixin
from .models import Category, Note, Transaction
from .services import month_from_query


class CategoryListView(OwnedQuerysetMixin, ListView):
    model = Category
    template_name = "expenses/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(OwnedFormMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "expenses/form.html"
    success_url = reverse_lazy("expenses:category_list")
    extra_context = {
        "title": "Thêm danh mục",
        "submit_label": "Lưu danh mục",
        "cancel_url": reverse_lazy("expenses:category_list"),
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Đã thêm danh mục.")
        return response


class CategoryUpdateView(OwnedQuerysetMixin, OwnedFormMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "expenses/form.html"
    success_url = reverse_lazy("expenses:category_list")
    extra_context = {
        "title": "Sửa danh mục",
        "submit_label": "Cập nhật",
        "cancel_url": reverse_lazy("expenses:category_list"),
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Đã cập nhật danh mục.")
        return response


class CategoryDeleteView(OwnedQuerysetMixin, DeleteView):
    model = Category
    template_name = "expenses/confirm_delete.html"
    success_url = reverse_lazy("expenses:category_list")
    extra_context = {
        "title": "Xóa danh mục",
        "cancel_url": reverse_lazy("expenses:category_list"),
    }

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "Không xóa được: danh mục đang được dùng bởi giao dịch.",
            )
            return redirect("expenses:category_list")
        messages.success(self.request, "Đã xóa danh mục.")
        return response


class TransactionListView(OwnedQuerysetMixin, ListView):
    model = Transaction
    template_name = "expenses/transaction_list.html"
    context_object_name = "transactions"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related("category")
        year, month = month_from_query(self.request.GET)
        kind = self.request.GET.get("kind") or ""
        category_id = self.request.GET.get("category") or ""
        qs = qs.filter(occurred_on__year=year, occurred_on__month=month)
        if kind:
            qs = qs.filter(category__kind=kind)
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["year"], ctx["month"] = month_from_query(self.request.GET)
        ctx["kind"] = self.request.GET.get("kind") or ""
        ctx["selected_category"] = self.request.GET.get("category") or ""
        ctx["categories"] = Category.objects.filter(user=self.request.user)
        ctx["kind_choices"] = Category.Kind.choices
        return ctx


class TransactionCreateView(OwnedFormMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "expenses/form.html"
    success_url = reverse_lazy("expenses:transaction_list")
    extra_context = {
        "title": "Thêm giao dịch",
        "submit_label": "Lưu giao dịch",
        "cancel_url": reverse_lazy("expenses:transaction_list"),
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Đã thêm giao dịch.")
        return response


class TransactionUpdateView(OwnedQuerysetMixin, OwnedFormMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "expenses/form.html"
    success_url = reverse_lazy("expenses:transaction_list")
    extra_context = {
        "title": "Sửa giao dịch",
        "submit_label": "Cập nhật",
        "cancel_url": reverse_lazy("expenses:transaction_list"),
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Đã cập nhật giao dịch.")
        return response


class TransactionDeleteView(OwnedQuerysetMixin, DeleteView):
    model = Transaction
    template_name = "expenses/confirm_delete.html"
    success_url = reverse_lazy("expenses:transaction_list")
    extra_context = {
        "title": "Xóa giao dịch",
        "cancel_url": reverse_lazy("expenses:transaction_list"),
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Đã xóa giao dịch.")
        return response


class NoteListView(OwnedQuerysetMixin, ListView):
    model = Note
    template_name = "expenses/note_list.html"
    context_object_name = "notes"


class NoteCreateView(OwnedFormMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "expenses/form.html"
    success_url = reverse_lazy("expenses:note_list")
    extra_context = {
        "title": "Thêm ghi chú",
        "submit_label": "Lưu ghi chú",
        "cancel_url": reverse_lazy("expenses:note_list"),
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Đã lưu ghi chú.")
        return response


class NoteUpdateView(OwnedQuerysetMixin, OwnedFormMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "expenses/form.html"
    success_url = reverse_lazy("expenses:note_list")
    extra_context = {
        "title": "Sửa ghi chú",
        "submit_label": "Cập nhật",
        "cancel_url": reverse_lazy("expenses:note_list"),
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Đã cập nhật ghi chú.")
        return response


class NoteDeleteView(OwnedQuerysetMixin, DeleteView):
    model = Note
    template_name = "expenses/confirm_delete.html"
    success_url = reverse_lazy("expenses:note_list")
    extra_context = {
        "title": "Xóa ghi chú",
        "cancel_url": reverse_lazy("expenses:note_list"),
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Đã xóa ghi chú.")
        return response
