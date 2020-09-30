from assign_rights.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


class LoggedInMixinDefaults(LoginRequiredMixin):
    login_url = reverse_lazy("login")


class UserMixin(LoggedInMixinDefaults, UserPassesTestMixin):
    authenticated_redirect_url = reverse_lazy("login")

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class EditMixin(UserMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='edit').exists()


class DeleteMixin(UserMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='delete').exists()
