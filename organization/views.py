from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from organization import models, forms


class ViewListOrganizations(LoginRequiredMixin, ListView):
    """
    :return List of Organizations for one user
    """
    model = models.Organization
    template_name = 'list-organizations.html'

    def get_queryset(self):
        organizations = models.Organization.objects.filter(creator=self.request.user)
        return organizations


class ViewDetailOrganization(LoginRequiredMixin, DetailView):
    """
    :return one organization
    """
    model = models.Organization
    template_name = 'detail-organization.html'

    def get_queryset(self):
        organization = models.Organization.objects.filter(slug=self.kwargs['slug'], creator=self.request.user)
        return organization


class ViewEditOrganization(LoginRequiredMixin, UpdateView):
    """
    view for edit one organization
    """
    model = models.Organization
    template_name = 'edit-organization.html'
    form_class = forms.OrganizationEditForm

    def get_queryset(self):
        organization = models.Organization.objects.filter(slug=self.kwargs['slug'], creator=self.request.user)
        return organization

    def get_success_url(self):
        return reverse('organizations:detail-organization', kwargs={'slug': self.object.slug})


class ViewCreateOrganization(LoginRequiredMixin, CreateView):
    """
    create new organization
    """
    models = models.Organization
    form_class = forms.OrganizationCreateForm
    template_name = 'create-organization.html'

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw.update({'creator': self.request.user})
        return kw

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('organizations:list-organizations')
