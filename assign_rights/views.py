from assign_rights.models import RightsShell, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)
from rest_framework.response import Response
from rest_framework.views import APIView

from .assemble import RightsAssembler
from .forms import RightsGrantedFormSet, RightsShellForm


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


class RightsShellListView(ListView):
    '''browse and search rights shells'''
    queryset = RightsShell.objects.all()


class RightsShellCreateView(CreateView):
    model = RightsShell
    template_name = "assign_rights/rightsshell_create.html"
    form_class = RightsShellForm
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(RightsShellCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['rights_granted'] = RightsGrantedFormSet(self.request.POST)
        else:
            context['rights_granted'] = RightsGrantedFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        rights_granted = context['rights_granted']
        if rights_granted.is_valid():
            response = super().form_valid(form)
            rights_granted.instance = self.object
            rights_granted.save()
            return response
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("rights-detail", kwargs={"pk": self.object.pk})


class RightsShellDetailView(DetailView):
    '''view a rights shell'''
    queryset = RightsShell.objects.all()


class RightsShellUpdateView(UpdateView):
    model = RightsShell
    template_name = "assign_rights/rightsshell_create.html"
    form_class = RightsShellForm
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(RightsShellCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['rights_granted'] = RightsGrantedFormSet(self.request.POST, instance=self.object)
        else:
            context['rights_granted'] = RightsGrantedFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        rights_granted = context['rights_granted']
        if rights_granted.is_valid():
            response = super.form_valid(form)
            rights_granted.instance = self.object
            rights_granted.save()
            return response
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("rights-detail", kwargs={"pk": self.object.pk})


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
