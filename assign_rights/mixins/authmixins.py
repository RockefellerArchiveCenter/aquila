from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


class LoggedInMixinDefaults(LoginRequiredMixin):
    """Sets basic login_url for mixin defaults."""
    login_url = reverse_lazy("login")


class EditMixin(LoggedInMixinDefaults, UserPassesTestMixin):
    """Checks whether a user is either a superuser or in the edit group."""

    def test_func(self):
        return any([
            self.request.user.is_superuser,
            self.request.user.groups.filter(name='edit').exists()
        ])


class DeleteMixin(LoggedInMixinDefaults, UserPassesTestMixin):
    """Checks whether a user is either a superuser or in the delete group."""

    def test_func(self):
        return any([
            self.request.user.is_superuser,
            self.request.user.groups.filter(name='delete').exists()
        ])
