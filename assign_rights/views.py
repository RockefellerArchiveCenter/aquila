from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class RightsShellsListView(ListView):
    '''browse and search rights shells'''
    pass


class RightsShellsCreateView(CreateView):
    '''create rights shells'''
    pass


class RightsShellsDetailView(DetailView):
    '''view a rights shell'''
    pass


class RightsShellsUpdateView(UpdateView):
    '''update rights shell'''
    pass


class GroupingsListView(ListView):
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
