from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from organization import models, forms, serializers
from organization.models import OrganizationProduct


class ViewListOrganizations(LoginRequiredMixin, ListView):
    """
    view for List of Organizations for one user
    """
    model = models.Organization
    template_name = 'list-organizations.html'

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        mode = self.request.GET.get('mode', None)
        if mode == 'name':
            organizations = models.Organization.objects.filter(name__contains=search, creator=self.request.user)
        elif mode == 'city':
            organizations = models.Organization.objects.filter(city__contains=search, creator=self.request.user)
        elif mode == 'purchasing_officer_name':
            organizations = models.Organization.objects.filter(purchasing_officer_name__contains=search,
                                                               creator=self.request.user)
        elif mode == 'purchasing_officer_number':
            organizations = models.Organization.objects.filter(purchasing_officer_phone_number__contains=search,
                                                               creator=self.request.user)
        else:
            organizations = models.Organization.objects.filter(creator=self.request.user)
        return organizations


class ViewDetailOrganization(LoginRequiredMixin, DetailView):
    """
    view for show one organization with detail
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

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid input.')
        return redirect(reverse('organizations:edit-organization', kwargs={'slug': self.object.slug}))

    def form_valid(self, form):
        try:
            messages.success(self.request, 'Organization edited successfully.')
            return super().form_valid(form)
        except:
            messages.error(self.request, 'Invalid input.')
            return redirect(reverse_lazy('organizations:edit-organization'))

    def get_success_url(self):
        return reverse('organizations:detail-organization', kwargs={'slug': self.object.slug})


class ViewCreateOrganization(LoginRequiredMixin, CreateView):
    """
    view for create new organization
    """
    form_class = forms.OrganizationCreateForm
    template_name = 'create-organization.html'
    extra_context = {'organization_products': OrganizationProduct.objects.all()}

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw.update({'creator': self.request.user})
        return kw

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid input.')
        return reverse_lazy('organizations:create-organization')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        try:
            messages.success(self.request, 'Organization created successfully.')
            return super().form_valid(form)
        except:
            messages.error(self.request, 'Invalid input.')
            return redirect(reverse_lazy('organizations:create-organization'))

    def get_success_url(self):
        return reverse('organizations:list-organizations')


# API


class APIListOrganization(ListAPIView):
    """
    API with jwt for show all organization for one user
    """
    serializer_class = serializers.OrganizationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = models.Organization.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(creator=self.request.user)
