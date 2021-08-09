from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from organization import models, forms, serializers
from organization.models import OrganizationProduct
from django.utils.translation import ugettext_lazy as _


class OrganizationsListView(LoginRequiredMixin, ListView):
    """
    view for List of Organizations for one user
    """
    model = models.Organization
    template_name = 'list-organizations.html'
    paginate_by = 10

    def get_queryset(self):
        """
        give a list of organization for one user and search on organizations
        """
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
        return organizations.order_by('-id')


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    """
    view for show one organization with detail
    """
    model = models.Organization
    template_name = 'detail-organization.html'

    def get_queryset(self):
        """
        check organization creator and request user
        """
        organization = models.Organization.objects.filter(slug=self.kwargs['slug'], creator=self.request.user)
        return organization


class OrganizationEditView(LoginRequiredMixin, UpdateView):
    """
    view for edit one organization
    """
    model = models.Organization
    template_name = 'edit-organization.html'
    form_class = forms.OrganizationEditForm

    def get_queryset(self):
        """
        check organization creator and request user
        """
        organization = models.Organization.objects.filter(slug=self.kwargs['slug'], creator=self.request.user)
        return organization

    def form_invalid(self, form):
        messages.error(self.request, _('Invalid input.'))
        response = super().form_invalid(form)
        response.status_code = 400
        return response

    def form_valid(self, form):
        messages.success(self.request, _('Organization edited successfully.'))
        return super().form_valid(form)

    def get_success_url(self):
        """
        back to detail view
        """
        return reverse_lazy('organizations:detail-organization', kwargs={'slug': self.object.slug})


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    """
    view for create new organization
    """
    form_class = forms.OrganizationCreateForm
    template_name = 'create-organization.html'
    extra_context = {'organization_products': OrganizationProduct.objects.all()}
    success_url = reverse_lazy('organizations:list-organizations')

    def get_form_kwargs(self):
        """
        add request user to form
        """
        kw = super().get_form_kwargs()
        kw.update({'creator': self.request.user})
        return kw

    def form_invalid(self, form):
        messages.error(self.request, _('Invalid input.'))
        response = super().form_invalid(form)
        response.status_code = 400
        return response

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, _('Organization created successfully.'))
        return super().form_valid(form)


# API


class OrganizationViewSetAPI(ModelViewSet):
    """
    API with jwt for show all organization for one user
    """
    serializer_class = serializers.OrganizationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = models.Organization.objects.all()

    def get_queryset(self):
        """
        list of organization for one user
        """
        qs = super().get_queryset()
        return qs.filter(creator=self.request.user)

    def perform_create(self, serializer):
        """
        add request user to serializer
        """
        serializer.save(creator=self.request.user)
