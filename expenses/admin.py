from django.contrib import admin

from .models import Category, Note, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "user", "color")
    list_filter = ("kind",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("occurred_on", "category", "amount", "user", "note")
    list_filter = ("category__kind", "occurred_on")
    search_fields = ("note", "category__name")


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    search_fields = ("content", "user__username")
