from django.urls import path

from . import views

app_name = "expenses"

urlpatterns = [
    path("danh-muc/", views.CategoryListView.as_view(), name="category_list"),
    path("danh-muc/them/", views.CategoryCreateView.as_view(), name="category_create"),
    path("danh-muc/<int:pk>/sua/", views.CategoryUpdateView.as_view(), name="category_update"),
    path("danh-muc/<int:pk>/xoa/", views.CategoryDeleteView.as_view(), name="category_delete"),
    path("giao-dich/", views.TransactionListView.as_view(), name="transaction_list"),
    path("giao-dich/them/", views.TransactionCreateView.as_view(), name="transaction_create"),
    path("giao-dich/<int:pk>/sua/", views.TransactionUpdateView.as_view(), name="transaction_update"),
    path("giao-dich/<int:pk>/xoa/", views.TransactionDeleteView.as_view(), name="transaction_delete"),
    path("ghi-chu/", views.NoteListView.as_view(), name="note_list"),
    path("ghi-chu/them/", views.NoteCreateView.as_view(), name="note_create"),
    path("ghi-chu/<int:pk>/sua/", views.NoteUpdateView.as_view(), name="note_update"),
    path("ghi-chu/<int:pk>/xoa/", views.NoteDeleteView.as_view(), name="note_delete"),
]
