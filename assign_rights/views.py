from assign_rights.models import RightsShell, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)
from rest_framework.response import Response
from rest_framework.views import APIView

from .assemble import RightsAssembler
from .forms import RightsShellModelForm


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


def RightsShellListView(ListView):
    '''browse and search rights shells'''
    queryset = RightsShell.objects.all()


class RightsShellCreateView(CreateView):
    '''create rights shells'''
    template_name = "assign_rights/rightsshell_create.html"
    form_class = RightsShellModelForm
    queryset = RightsShell.objects.all()

    def form_valid(self, form):
        """docstring for form_valid"""
        print(form.cleaned_data)
        return super().form_valid(form)


class RightsShellDetailView(DetailView):
    '''view a rights shell'''
    pass


class RightsShellUpdateView(UpdateView):
    '''update rights shell'''
    pass


class GroupingsListView(ListView):
    '''browse and search groupings'''
    pass


class GroupingsCreateView(CreateView):
    '''create groupings'''
    pass


class GroupingsDetailView(DetailView):
    '''view a grouping'''
    pass


class GroupingsUpdateView(UpdateView):
    '''update grouping'''
    pass


class AquilaLoginView(PageTitleMixin, LoginView):
    """Custom Login View to set page title."""
    page_title = "Login"


class RightsAssemblerView(APIView):
    """Calls the RightsAssembler class from assemblers."""

    def post(self, request, format=None):
        rights_ids = request.data.get("identifiers")
        end_date = request.data.get("end_date")
        assembled = RightsAssembler().run(rights_ids, end_date)
        return Response(assembled)


class LoggedInView(PageTitleMixin, LoginRequiredMixin, TemplateView):
    template_name = "users/logged_in.html"

    def get_page_title(self, context):
        return("You are logged in, {}!".format(self.request.user.username))
