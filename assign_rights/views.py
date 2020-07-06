from assign_rights.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)


class PageTitleMixin(object):
    """Sets the page_title key in view data.

    On views where this mixin is added, page titles can be set either by providing
    a page_title attribute or a get_page_title method.
    """

    def get_page_title(self, context):
        return getattr(self, "page_title", "Default Page Title")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.get_page_title(context)
        return context


def RightsShellsListView(ListView):
    '''browse and search rights shells'''
    pass


def RightsShellsCreateView(CreateView):
    '''create rights shells'''
    pass


def RightsShellsDetailView(DetailView):
    '''view a rights shell'''
    pass


def RightsShellsUpdateView(UpdateView):
    '''update rights shell'''
    pass


def GroupingsListView(ListView):
    '''browse and search groupings'''
    pass


def GroupingsCreateView(CreateView):
    '''create groupings'''
    pass


def GroupingsDetailView(DetailView):
    '''view a grouping'''
    pass


def GroupingsUpdateView(UpdateView):
    '''update grouping'''
    pass


class AquilaLoginView(PageTitleMixin, LoginView):
    page_title = "Login"


class LoggedInView(PageTitleMixin, LoginRequiredMixin, TemplateView):
    template_name = "users/logged_in.html"

    def get_page_title(self, context):
        return("You are logged in, {}!".format(self.request.user.username))
