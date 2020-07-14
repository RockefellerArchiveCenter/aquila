from assign_rights.models import RightsShell, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rest_framework.response import Response
from rest_framework.views import APIView

from .assemble import RightsAssembler
from .forms import GroupingForm, RightsGrantedFormSet, RightsShellForm
from .models import Grouping


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


class RightsShellListView(LoginRequiredMixin, ListView):
    '''browse and search rights shells'''
    queryset = RightsShell.objects.all()
    template_name = "rights/list.html"


class RightsShellCreateView(LoginRequiredMixin, CreateView):
    model = RightsShell
    template_name = "rights/manage.html"
    form_class = RightsShellForm
    success_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class RightsShellDetailView(LoginRequiredMixin, DetailView):
    '''view a rights shell'''
    queryset = RightsShell.objects.all()
    template_name = "rights/detail.html"


class RightsShellUpdateView(LoginRequiredMixin, UpdateView):
    model = RightsShell
    template_name = "rights/manage.html"
    form_class = RightsShellForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['rights_granted_form'] = RightsGrantedFormSet(self.request.POST, instance=self.object)
        else:
            context['rights_granted_form'] = RightsGrantedFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        rights_granted = context['rights_granted']
        if rights_granted_form.is_valid():
            response = super().form_valid(form)
            rights_granted_form.instance = self.object
            rights_granted.save()
            return response
        else:
            return super().form_invalid(form)



class GroupingListView(PageTitleMixin, LoginRequiredMixin, ListView):
    """Browse and search groupings."""
    model = Grouping
    template_name = "groupings/list.html"
    page_title = "Groupings"


class GroupingCreateView(PageTitleMixin, LoginRequiredMixin, CreateView):
    """Create a grouping."""
    model = Grouping
    template_name = "groupings/manage.html"
    form_class = GroupingForm
    page_title = "Create New Grouping"


class GroupingDetailView(PageTitleMixin, LoginRequiredMixin, DetailView):
    """View a grouping."""
    model = Grouping
    template_name = "groupings/detail.html"

    def get_page_title(self, context):
        return context["object"].title


class GroupingUpdateView(PageTitleMixin, LoginRequiredMixin, UpdateView):
    """Update a grouping."""
    model = Grouping
    template_name = "groupings/manage.html"
    form_class = GroupingForm

    def get_page_title(self, context):
        return "Update {}".format(context["object"].title)


class AquilaLoginView(PageTitleMixin, LoginView):
    """Custom Login View to set page title."""
    page_title = "Login"


class RightsAssemblerView(APIView):
    """Calls the RightsAssembler class from assemblers."""

    def post(self, request, format=None):
        rights_ids = request.data.get("identifiers")
        request_start_date = request.data.get("start_date")
        request_end_date = request.data.get("end_date")
        assembled = RightsAssembler().run(rights_ids, request_start_date, request_end_date)
        return Response(assembled)
