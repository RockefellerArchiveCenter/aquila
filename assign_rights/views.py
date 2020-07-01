from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rest_framework.response import Response
from rest_framework.views import APIView

from .assemble import RightsAssembler


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


class GroupingsCreateView(CreateView):
    '''create groupings'''
    pass


class GroupingsDetailView(DetailView):
    '''view a grouping'''
    pass


class GroupingsUpdateView(UpdateView):
    '''update grouping'''
    pass

class RightsAssemblerView(APIView):
    '''
    Calls the RightsAssembler class from assemblers.
    '''
    def post(self, request, format=None):
        request_list = request.data.get('items')
        shell_list = RightsAssembler().run(request_list)
        print(shell_list)
        return Response(request_list, status=200)
