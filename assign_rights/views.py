from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView

from assign_rights.models import User


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


class LoggedInView(LoginRequiredMixin, TemplateView):
    template_name = "users/logged_in.html"
