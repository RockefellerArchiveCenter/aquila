from assign_rights.models import RightsShell
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rest_framework.response import Response
from rest_framework.views import APIView

from .assemble import RightsAssembler
from .forms import (CopyrightForm, GroupingForm, LicenseForm, OtherForm,
                    RightsGrantedFormSet, RightsShellForm, StatuteForm)
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


class RightsShellListView(PageTitleMixin, LoginRequiredMixin, ListView):
    """Browse and search rights shells."""
    model = RightsShell
    template_name = "rights/list.html"
    page_title = "Rights Shells"


class RightsShellCreateView(PageTitleMixin, LoginRequiredMixin, CreateView):
    """Create a rights shell."""
    model = RightsShell
    template_name = "rights/create.html"
    form_class = RightsShellForm
    page_title = "Create New Rights Shell"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['rights_granted_form'] = RightsGrantedFormSet(self.request.POST)
            context['copyright_form'] = CopyrightForm(self.request.POST)
            context['other_form'] = OtherForm(self.request.POST)
            context['statute_form'] = StatuteForm(self.request.POST)
            context['license_form'] = LicenseForm(self.request.POST)
        else:
            context['rights_granted_form'] = RightsGrantedFormSet()
            context['copyright_form'] = CopyrightForm()
            context['other_form'] = OtherForm()
            context['statute_form'] = StatuteForm()
            context['license_form'] = LicenseForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        rights_granted = context['rights_granted_form']
        if rights_granted.is_valid():
            response = super().form_valid(form)
            rights_granted.instance = self.object
            rights_granted.save()
            return response
        else:
            return super().form_invalid(form)


class RightsShellDetailView(PageTitleMixin, LoginRequiredMixin, DetailView):
    """View a rights shell."""
    model = RightsShell
    template_name = "rights/detail.html"

    def get_page_title(self, context):
        return "Rights Shell {}".format(context["object"].pk)


class RightsShellUpdateView(PageTitleMixin, LoginRequiredMixin, UpdateView):
    """Update a rights shell."""
    model = RightsShell
    template_name = "rights/edit.html"
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
        rights_granted_form = context['rights_granted_form']
        if rights_granted_form.is_valid():
            response = super().form_valid(form)
            rights_granted_form.instance = self.object
            rights_granted_form.save()
            return response
        else:
            return super().form_invalid(form)

    def get_page_title(self, context):
        return "Update Rights Shell {}".format(context["object"].pk)


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

    def post(self, request):
        rights_ids = request.data.get("identifiers")
        request_start_date = request.data.get("start_date")
        request_end_date = request.data.get("end_date")
        if not all([rights_ids, request_start_date, request_end_date]):
            return Response(
                {"detail": "Request data must contain 'identifiers', 'start_date' and 'end_date' keys."},
                status=500)
        try:
            rights = RightsAssembler().run(rights_ids, request_start_date, request_end_date)
            return Response({"rights_statements": rights}, status=200)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
