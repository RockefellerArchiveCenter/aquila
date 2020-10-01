from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


class LoggedInMixinDefaults(LoginRequiredMixin):
    """Sets basic login_url for mixin defaults"""
    login_url = reverse_lazy("login")


class UserMixin(LoggedInMixinDefaults, UserPassesTestMixin):
    """Overwrites the mixin defaults"""
    authenticated_redirect_url = reverse_lazy("login")

    def test_func(self):
        """Checks whether a user is a superuser in the application"""
        if self.request.user.is_superuser:
            return True
        return False


class EditMixin(UserMixin, UserPassesTestMixin):
    """Checks whether a user is in the edit group"""
    def test_func(self):
        return self.request.user.groups.filter(name='edit').exists()


class DeleteMixin(UserMixin, UserPassesTestMixin):
    """Checks whether a user is in the delete group"""
    def test_func(self):
        return self.request.user.groups.filter(name='delete').exists()
