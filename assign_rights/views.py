from assign_rights.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)
from rest_framework.response import Response
from rest_framework.views import APIView

from .assemble import RightsAssembler
from .models import Grouping


class RightsShellListView(ListView):
    '''browse and search rights shells'''
    pass


class RightsShellCreateView(CreateView):
    '''create rights shells'''
    pass


class RightsShellDetailView(DetailView):
    '''view a rights shell'''
    pass


class RightsShellUpdateView(UpdateView):
    '''update rights shell'''
    pass


class GroupingListView(ListView):
    """Browse and search groupings."""
    model = Grouping
    template_name = "groupings/list.html"


class GroupingsCreateView(CreateView):
    '''create groupings'''
    pass


class GroupingDetailView(DetailView):
    '''view a grouping'''
    pass


class GroupingUpdateView(UpdateView):
    '''update grouping'''
    pass


class RightsAssemblerView(APIView):
    '''
    Calls the RightsAssembler class from assemblers.
    '''

    def post(self, request, format=None):
        rights_ids = request.data.get("identifiers")
        end_date = request.data.get("end_date")
        assembled = RightsAssembler().run(rights_ids, end_date)
        return Response(assembled)


class LoggedInView(LoginRequiredMixin, TemplateView):
    template_name = "users/logged_in.html"
