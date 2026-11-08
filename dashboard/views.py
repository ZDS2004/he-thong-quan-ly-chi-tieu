from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from expenses.services import month_from_query, month_summary


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        year, month = month_from_query(self.request.GET)
        summary = month_summary(self.request.user, year, month)
        ctx["summary"] = summary
        ctx["year"] = year
        ctx["month"] = month
        ctx["chart_categories"] = {
            "labels": [row["name"] for row in summary.by_category],
            "values": [int(row["total"]) for row in summary.by_category],
            "colors": [row["color"] for row in summary.by_category],
        }
        ctx["chart_daily"] = {
            "labels": [row["day"] for row in summary.daily_expense],
            "values": [int(row["total"]) for row in summary.daily_expense],
        }
        return ctx
