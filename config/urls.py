from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("chi-tieu/", include("expenses.urls")),
    path("", include("dashboard.urls")),
]
