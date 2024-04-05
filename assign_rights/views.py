from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import (CopyrightForm, GroupingForm, LicenseForm, OtherForm,
                    RightsGrantedFormSet, RightsShellForm,
                    RightsShellUpdateForm, StatuteForm, StrErrorList)
from .mixins.authmixins import DeleteMixin, EditMixin
from .models import Grouping, RightsGranted, RightsShell


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


class HomePage(PageTitleMixin, LoginRequiredMixin, TemplateView):
    """Application landing page."""
    page_title = "Aquila 🦅"
    template_name = "index.html"


class RightsShellListView(PageTitleMixin, LoginRequiredMixin, ListView):
    """Browse and search rights statements."""
    model = RightsShell
    template_name = "rights/list.html"
    page_title = "Rights Statements"


class RightsShellCreateView(PageTitleMixin, EditMixin, CreateView):
    """Create a rights statement. Only available to 'edit' group."""
    model = RightsShell
    template_name = "rights/manage.html"
    form_class = RightsShellForm
    page_title = "Create New Rights Statement"

    def get_context_data(self, **kwargs):
        """Load specific rights basis form based on logic in rights create template. Returns subclass of RightsShellForm"""
        context = super().get_context_data(**kwargs)
        context["act_choices"] = RightsGranted.ACT_CHOICES
        context["restriction_choices"] = RightsGranted.RESTRICTION_CHOICES
        if self.request.POST:
            context['rights_granted_form'] = RightsGrantedFormSet(self.request.POST, error_class=StrErrorList)
            context['copyright_form'] = CopyrightForm(self.request.POST, error_class=StrErrorList)
            context['other_form'] = OtherForm(self.request.POST, error_class=StrErrorList)
            context['statute_form'] = StatuteForm(self.request.POST, error_class=StrErrorList)
            context['license_form'] = LicenseForm(self.request.POST, error_class=StrErrorList)
        else:
            context['rights_granted_form'] = RightsGrantedFormSet()
            context['copyright_form'] = CopyrightForm(initial={'jurisdiction': 'us'})
            context['other_form'] = OtherForm()
            context['statute_form'] = StatuteForm(initial={'jurisdiction': 'us'})
            context['license_form'] = LicenseForm()
        return context

    def form_valid(self, form):
        """Validates form based on specific type of rights basis (e.g., copyright).

        Args:
            form: subclass of RightsShellForm
        """
        context = self.get_context_data(form=form)
        rights_granted = context['rights_granted_form']
        if rights_granted.is_valid():
            response = super().form_valid(form)
            rights_granted.instance = self.object
            rights_granted.save()
            return response
        else:
            return super().form_invalid(form)


class RightsShellUpdateView(PageTitleMixin, EditMixin, UpdateView):
    """Update a rights statement. Only available to 'edit' group."""
    model = RightsShell
    template_name = "rights/manage.html"
    form_class = RightsShellUpdateForm

    def get_context_data(self, **kwargs):
        """Loads main rights basis form as well as inline formsets for rights granted or restricted."""
        context = super().get_context_data(**kwargs)
        form_cls = self.get_form_cls(context["object"].rights_basis)
        context["act_choices"] = RightsGranted.ACT_CHOICES
        context["restriction_choices"] = RightsGranted.RESTRICTION_CHOICES
        if self.request.POST:
            context["rights_granted_form"] = RightsGrantedFormSet(
                self.request.POST, instance=self.object, error_class=StrErrorList)
            context["basis_form"] = form_cls(self.request.POST, instance=self.object)
        else:
            context["rights_granted_form"] = RightsGrantedFormSet(instance=self.object)
            context["basis_form"] = form_cls(instance=self.object)
        return context

    def get_form_cls(self, rights_basis):
        """Returns the form class for a given rights basis."""
        if rights_basis == "copyright":
            form_cls = CopyrightForm
        elif rights_basis == "statute":
            form_cls = StatuteForm
        elif rights_basis == "license":
            form_cls = LicenseForm
        else:
            form_cls = OtherForm
        return form_cls

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
        return "Update {}".format(str(context["object"]))


class RightsShellDeleteView(PageTitleMixin, DeleteMixin, DeleteView):
    """Delete a rights statement."""
    model = RightsShell
    template_name = "rights/confirm_delete.html"
    page_title = "Confirm Delete"
    success_url = reverse_lazy("rights-list")


class RightsShellDetailView(PageTitleMixin, LoginRequiredMixin, DetailView):
    """View a rights statement."""
    model = RightsShell
    template_name = "rights/detail.html"

    def get_page_title(self, context):
        return str(context["object"])


class GroupingListView(PageTitleMixin, LoginRequiredMixin, ListView):
    """Browse and search groupings."""
    model = Grouping
    template_name = "groupings/list.html"
    page_title = "Groupings"


class GroupingCreateView(PageTitleMixin, EditMixin, CreateView):
    """Create a grouping. Only available to 'edit' group."""
    model = Grouping
    template_name = "groupings/manage.html"
    form_class = GroupingForm
    page_title = "Create New Grouping"


class GroupingDeleteView(PageTitleMixin, DeleteMixin, DeleteView):
    """Delete a grouping"""
    model = Grouping
    success_url = reverse_lazy("groupings-list")
    template_name = "groupings/confirm_delete.html"
    page_title = "Confirm Delete"


class GroupingDetailView(PageTitleMixin, LoginRequiredMixin, DetailView):
    """View a grouping."""
    model = Grouping
    template_name = "groupings/detail.html"

    def get_page_title(self, context):
        return context["object"].title


class GroupingUpdateView(PageTitleMixin, EditMixin, UpdateView):
    """Update a grouping. Only available to 'edit' group."""
    model = Grouping
    template_name = "groupings/manage.html"
    form_class = GroupingForm

    def get_page_title(self, context):
        return "Update {}".format(context["object"].title)


class AquilaLoginView(PageTitleMixin, LoginView):
    """Custom Login View to set page title."""
    page_title = "Login"

