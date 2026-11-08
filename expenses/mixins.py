from django.contrib.auth.mixins import LoginRequiredMixin


class OwnedQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OwnedFormMixin(LoginRequiredMixin):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)
